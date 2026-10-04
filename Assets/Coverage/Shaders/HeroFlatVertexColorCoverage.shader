// Copy of HeroRig/FlatVertexColor (do not edit the rig shader) plus UV3/UV4 coverage.
// UV3 = TEXCOORD2 (HEAD, SHLD, CHST, HAND). UV4 = TEXCOORD3 (LEGS, FEET, 0, 0).
// clip(_CoverageInset - hiddenScore) runs in every pass so colour, shadow, and depth agree.
Shader "HeroRig/FlatVertexColorCoverage"
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
        _HiddenRegions ("Hidden Regions", Float) = 0
        _CoverageInset ("Coverage Inset", Range(0, 1)) = 0.8
    }
    SubShader
    {
        Tags { "RenderType" = "Opaque" "RenderPipeline" = "UniversalPipeline" "Queue" = "Geometry" }

        HLSLINCLUDE
        #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
        #include "CoverageClip.hlsl"

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
            float _HiddenRegions;
            float _CoverageInset;
        CBUFFER_END
        ENDHLSL

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
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"

            struct Attributes
            {
                float4 positionOS : POSITION;
                float3 normalOS : NORMAL;
                half4 color : COLOR;
                float2 uv2 : TEXCOORD1;
                float4 uv3 : TEXCOORD2;
                float4 uv4 : TEXCOORD3;
            };
            struct Varyings
            {
                float4 positionCS : SV_POSITION;
                float3 positionWS : TEXCOORD0;
                float3 normalWS : TEXCOORD1;
                half4 color : COLOR;
                half fog : TEXCOORD2;
                float2 uv2 : TEXCOORD3;
                float4 cov3 : TEXCOORD4;
                float4 cov4 : TEXCOORD5;
            };

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
                o.cov3 = i.uv3;
                o.cov4 = i.uv4;
                return o;
            }

            half4 frag(Varyings i) : SV_Target
            {
                CoverageClip(_HiddenRegions, _CoverageInset, i.cov3, i.cov4);
                float3 n = normalize(i.normalWS);
                Light L = GetMainLight(TransformWorldToShadowCoord(i.positionWS));
                half ndl = saturate((dot(n, L.direction) + _Wrap) / (1.0h + _Wrap));
                half3 albedo = _BaseColor.rgb * lerp(half3(1, 1, 1), i.color.rgb, _VertexColorStrength);
                half3 lit = SampleSH(n) + L.color * (ndl * L.shadowAttenuation * L.distanceAttenuation);
                #if defined(_ADDITIONAL_LIGHTS)
                    InputData inputData = (InputData)0;
                    inputData.positionWS = i.positionWS;
                    inputData.normalWS = n;
                    inputData.viewDirectionWS = GetWorldSpaceNormalizeViewDir(i.positionWS);
                    inputData.normalizedScreenSpaceUV = GetNormalizedScreenSpaceUV(i.positionCS);
                    uint pixelLightCount = GetAdditionalLightsCount();
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

        Pass
        {
            Name "ShadowCaster"
            Tags { "LightMode" = "ShadowCaster" }
            ZWrite On
            ZTest LEqual
            ColorMask 0
            Cull Back
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma multi_compile_vertex _ _CASTING_PUNCTUAL_LIGHT_SHADOW
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Shadows.hlsl"

            float3 _LightDirection;
            float3 _LightPosition;

            struct Attributes
            {
                float4 positionOS : POSITION;
                float3 normalOS : NORMAL;
                float4 uv3 : TEXCOORD2;
                float4 uv4 : TEXCOORD3;
            };
            struct Varyings
            {
                float4 positionCS : SV_POSITION;
                float4 cov3 : TEXCOORD0;
                float4 cov4 : TEXCOORD1;
            };

            Varyings vert(Attributes i)
            {
                Varyings o;
                float3 positionWS = TransformObjectToWorld(i.positionOS.xyz);
                float3 normalWS = TransformObjectToWorldNormal(i.normalOS);
                #if _CASTING_PUNCTUAL_LIGHT_SHADOW
                    float3 lightDirectionWS = normalize(_LightPosition - positionWS);
                #else
                    float3 lightDirectionWS = _LightDirection;
                #endif
                float4 positionCS = TransformWorldToHClip(ApplyShadowBias(positionWS, normalWS, lightDirectionWS));
                o.positionCS = ApplyShadowClamping(positionCS);
                o.cov3 = i.uv3;
                o.cov4 = i.uv4;
                return o;
            }

            half4 frag(Varyings i) : SV_Target
            {
                CoverageClip(_HiddenRegions, _CoverageInset, i.cov3, i.cov4);
                return 0;
            }
            ENDHLSL
        }

        Pass
        {
            Name "DepthOnly"
            Tags { "LightMode" = "DepthOnly" }
            ZWrite On
            ColorMask R
            Cull Back
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            struct Attributes
            {
                float4 positionOS : POSITION;
                float4 uv3 : TEXCOORD2;
                float4 uv4 : TEXCOORD3;
            };
            struct Varyings
            {
                float4 positionCS : SV_POSITION;
                float4 cov3 : TEXCOORD0;
                float4 cov4 : TEXCOORD1;
            };

            Varyings vert(Attributes i)
            {
                Varyings o;
                o.positionCS = TransformObjectToHClip(i.positionOS.xyz);
                o.cov3 = i.uv3;
                o.cov4 = i.uv4;
                return o;
            }

            half frag(Varyings i) : SV_Target
            {
                CoverageClip(_HiddenRegions, _CoverageInset, i.cov3, i.cov4);
                return i.positionCS.z;
            }
            ENDHLSL
        }

        Pass
        {
            Name "DepthNormals"
            Tags { "LightMode" = "DepthNormals" }
            ZWrite On
            Cull Back
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            struct Attributes
            {
                float4 positionOS : POSITION;
                float3 normalOS : NORMAL;
                float4 uv3 : TEXCOORD2;
                float4 uv4 : TEXCOORD3;
            };
            struct Varyings
            {
                float4 positionCS : SV_POSITION;
                float3 normalWS : TEXCOORD0;
                float4 cov3 : TEXCOORD1;
                float4 cov4 : TEXCOORD2;
            };

            Varyings vert(Attributes i)
            {
                Varyings o;
                o.positionCS = TransformObjectToHClip(i.positionOS.xyz);
                o.normalWS = TransformObjectToWorldNormal(i.normalOS);
                o.cov3 = i.uv3;
                o.cov4 = i.uv4;
                return o;
            }

            half4 frag(Varyings i) : SV_Target
            {
                CoverageClip(_HiddenRegions, _CoverageInset, i.cov3, i.cov4);
                return half4(NormalizeNormalPerPixel(i.normalWS), 0.0);
            }
            ENDHLSL
        }
    }
    FallBack Off
}
