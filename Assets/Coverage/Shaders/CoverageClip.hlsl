#ifndef HERO_COVERAGE_CLIP_INCLUDED
#define HERO_COVERAGE_CLIP_INCLUDED

// hiddenScore = sum of region scores whose bit is set in _HiddenRegions.
// clip(inset - hiddenScore) discards only when the score is above the inset,
// so a declared region hides slightly less than its full extent.
float CoverageHiddenScore(float hiddenRegions, float4 uv3, float4 uv4)
{
    int m = (int)(hiddenRegions + 0.5);
    float s = 0.0;
    if ((m & 1) != 0) s += uv3.x;
    if ((m & 2) != 0) s += uv3.y;
    if ((m & 4) != 0) s += uv3.z;
    if ((m & 8) != 0) s += uv3.w;
    if ((m & 16) != 0) s += uv4.x;
    if ((m & 32) != 0) s += uv4.y;
    return s;
}

void CoverageClip(float hiddenRegions, float inset, float4 uv3, float4 uv4)
{
    clip(inset - CoverageHiddenScore(hiddenRegions, uv3, uv4));
}

#endif
