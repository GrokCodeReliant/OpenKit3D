// Character shader: flat (faceted) lit colour x baked vertex-colour AO / cloth gradient. Matte - no specular,
// no normal maps. Main directional light with soft wrap + shadows, spherical-harmonics ambient, fog.
// Pass 4: additional lights use the same wrap Lambert (no specular) so fill and rim show. The main-light term is unchanged.
// PC renderer is Forward+ (cluster light loop). _FORWARD_PLUS is kept for older URP variants.
Shader "HeroRig/FlatVertexColor"
{
    Properties
    {
        _BaseColor ("Base Color", Color) = (1, 1, 1, 1)
        _VertexColorStrength ("Vertex Colour (AO) Strength", Range(0, 1)) = 1
        _Wrap ("Light Wrap", Range(0, 1)) = 0.2
        _Wear ("Wear", Range(0, 1)) = 0
        _Finish ("Finish", Range(0, 1)) = 0
        _Emissive ("Emissive", Range(0, 2)) = 0
        _EmissiveColor ("Emissive Color", Color) = (1, 0.6, 0.2, 1)
        _Prismatic ("Prismatic", Float) = 0
        _Sweep ("Secondary Hue Sweep", Float) = 0
    }
    SubShader
    {
        Tags { "RenderType" = "Opaque" "RenderPipeline" = "UniversalPipeline" "Queue" = "Geometry" }
        Pass
        {
            Name "ForwardLit"
            Tags { "LightMode" = "UniversalForward" }
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma multi_compile _ _MAIN_LIGHT_SHADOWS _MAIN_LIGHT_SHADOWS_CASCADE _MAIN_LIGHT_SHADOWS_SCREEN
            #pragma multi_compile_fragment _ _SHADOWS_SOFT _SHADOWS_SOFT_LOW _SHADOWS_SOFT_MEDIUM _SHADOWS_SOFT_HIGH
            #pragma multi_compile _ _ADDITIONAL_LIGHTS_VERTEX _ADDITIONAL_LIGHTS
            #pragma multi_compile _ _CLUSTER_LIGHT_LOOP
            #pragma multi_compile _ _FORWARD_PLUS
            #pragma multi_compile_fog
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"

            CBUFFER_START(UnityPerMaterial)
                half4 _BaseColor;
                half4 _EmissiveColor;
                half _VertexColorStrength;
                half _Wrap;
                half _Wear;
                half _Finish;
                half _Emissive;
                half _Prismatic;
                half _Sweep;
            CBUFFER_END

            struct Attributes { float4 positionOS : POSITION; float3 normalOS : NORMAL; half4 color : COLOR; float2 uv2 : TEXCOORD1; };
            struct Varyings { float4 positionCS : SV_POSITION; float3 positionWS : TEXCOORD0; float3 normalWS : TEXCOORD1; half4 color : COLOR; half fog : TEXCOORD2; float2 uv2 : TEXCOORD3; };

            half3 HsvToRgb(half3 c)
            {
                half4 K = half4(1.0h, 2.0h / 3.0h, 1.0h / 3.0h, 3.0h);
                half3 p = abs(frac(c.xxx + K.xyz) * 6.0h - K.www);
                return c.z * lerp(K.xxx, saturate(p - K.xxx), c.y);
            }

            half3 RgbToHsv(half3 c)
            {
                half4 K = half4(0.0h, -1.0h / 3.0h, 2.0h / 3.0h, -1.0h);
                half4 p = lerp(half4(c.bg, K.wz), half4(c.gb, K.xy), step(c.b, c.g));
                half4 q = lerp(half4(p.xyw, c.r), half4(c.r, p.yzx), step(p.x, c.r));
                half d = q.x - min(q.w, q.y);
                half e = 1.0e-4h;
                return half3(abs(q.z + (q.w - q.y) / (6.0h * d + e)), d / (q.x + e), q.x);
            }

            Varyings vert(Attributes i)
            {
                Varyings o;
                VertexPositionInputs p = GetVertexPositionInputs(i.positionOS.xyz);
                o.positionCS = p.positionCS; o.positionWS = p.positionWS;
                o.normalWS = TransformObjectToWorldNormal(i.normalOS);
                o.color = i.color;
                o.fog = ComputeFogFactor(p.positionCS.z);
                o.uv2 = i.uv2;
                return o;
            }

            half4 frag(Varyings i) : SV_Target
            {
                float3 n = normalize(i.normalWS);
                Light L = GetMainLight(TransformWorldToShadowCoord(i.positionWS));
                half ndl = saturate((dot(n, L.direction) + _Wrap) / (1.0h + _Wrap));
                half3 albedo = _BaseColor.rgb * lerp(half3(1, 1, 1), i.color.rgb, _VertexColorStrength);
                // main light: identical to pass 3
                half3 lit = SampleSH(n) + L.color * (ndl * L.shadowAttenuation * L.distanceAttenuation);
                #if defined(_ADDITIONAL_LIGHTS)
                    InputData inputData = (InputData)0;
                    inputData.positionWS = i.positionWS;
                    inputData.normalWS = n;
                    inputData.viewDirectionWS = GetWorldSpaceNormalizeViewDir(i.positionWS);
                    inputData.normalizedScreenSpaceUV = GetNormalizedScreenSpaceUV(i.positionCS);
                    uint pixelLightCount = GetAdditionalLightsCount();
                    // Forward+: extra directionals (fill, rim) live in this loop; the main light is not in it.
                    #if USE_CLUSTER_LIGHT_LOOP
                    [loop] for (uint lightIndex = 0u; lightIndex < min(URP_FP_DIRECTIONAL_LIGHTS_COUNT, MAX_VISIBLE_LIGHTS); lightIndex++)
                    {
                        Light addL = GetAdditionalLight(lightIndex, i.positionWS);
                        half ndlA = saturate((dot(n, addL.direction) + _Wrap) / (1.0h + _Wrap));
                        lit += addL.color * (ndlA * addL.shadowAttenuation * addL.distanceAttenuation);
                    }
                    #endif
                    LIGHT_LOOP_BEGIN(pixelLightCount)
                        Light addL = GetAdditionalLight(lightIndex, i.positionWS);
                        half ndlA = saturate((dot(n, addL.direction) + _Wrap) / (1.0h + _Wrap));
                        lit += addL.color * (ndlA * addL.shadowAttenuation * addL.distanceAttenuation);
                    LIGHT_LOOP_END
                #endif
                // Defaults are zero, so every existing character material takes this path unchanged.
                half3 rgb = albedo * lit;
                if (_Wear != 0.0h || _Finish != 0.0h || _Emissive != 0.0h || _Prismatic != 0.0h || _Sweep != 0.0h)
                {
                    half3 tint = albedo;
                    if (_Prismatic != 0.0h && _Sweep > 0.5h)
                    {
                        half3 hsv = RgbToHsv(tint);
                        hsv.x = frac(i.positionWS.y * 0.45h + _Time.y * 0.15h);
                        tint = HsvToRgb(hsv);
                    }
                    half mask = saturate(i.uv2.x);
                    half w = mask * _Wear;
                    if (w > 0.0h)
                    {
                        half luma = dot(tint, half3(0.299h, 0.587h, 0.114h));
                        half3 desat = lerp(tint, luma.xxx, w);
                        tint = lerp(desat, half3(0.22745h, 0.20000h, 0.16863h), w);
                        tint *= lerp(1.0h, 0.55h, w);
                    }
                    rgb = tint * lit;
                    if (_Finish > 0.0h)
                    {
                        float3 viewDir = GetWorldSpaceNormalizeViewDir(i.positionWS);
                        half ndv = saturate(dot(n, viewDir));
                        half fres = pow(1.0h - ndv, 3.0h);
                        float3 halfDir = normalize(L.direction + viewDir);
                        half spec = pow(saturate(dot(n, halfDir)), 32.0h);
                        rgb += (spec * L.color + fres) * _Finish * L.shadowAttenuation;
                    }
                    if (_Emissive > 0.0h)
                    {
                        half3 emis = _EmissiveColor.rgb;
                        if (_Prismatic != 0.0h)
                            emis = HsvToRgb(half3(frac(_Time.y * 0.25h), 0.75h, 1.0h));
                        rgb += emis * _Emissive;
                    }
                }
                return half4(MixFog(rgb, i.fog), 1);
            }
            ENDHLSL
        }
        UsePass "Universal Render Pipeline/Lit/ShadowCaster"
        UsePass "Universal Render Pipeline/Lit/DepthOnly"
        UsePass "Universal Render Pipeline/Lit/DepthNormals"
    }
    FallBack Off
}
