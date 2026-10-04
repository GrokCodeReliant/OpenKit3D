Shader "HeroRig/Overlay"
{
    Properties { _Color ("Color", Color) = (1,1,1,1) _MainTex ("Texture", 2D) = "white" {} }
    SubShader
    {
        Tags { "Queue"="Overlay" "RenderType"="Transparent" "RenderPipeline"="UniversalPipeline" }
        Pass
        {
            Tags { "LightMode"="SRPDefaultUnlit" }
            ZTest Always ZWrite Off Cull Off Blend SrcAlpha OneMinusSrcAlpha
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            TEXTURE2D(_MainTex); SAMPLER(sampler_MainTex);
            CBUFFER_START(UnityPerMaterial) float4 _Color; float4 _MainTex_ST; CBUFFER_END
            struct A { float4 pos : POSITION; float4 col : COLOR; float2 uv : TEXCOORD0; };
            struct V { float4 pos : SV_POSITION; float4 col : COLOR; float2 uv : TEXCOORD0; };
            V vert(A i) { V o; o.pos = TransformObjectToHClip(i.pos.xyz); o.col = i.col * _Color; o.uv = i.uv; return o; }
            half4 frag(V i) : SV_Target { half4 c = i.col; c.a *= SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, i.uv).a; return c; }
            ENDHLSL
        }
    }
}
