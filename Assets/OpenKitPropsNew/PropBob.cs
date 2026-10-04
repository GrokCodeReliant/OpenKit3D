using UnityEngine;

namespace OpenKitPropsNew
{
    /// <summary>Slow hover and spin for pickup props. CC0.</summary>
    public class PropBob : MonoBehaviour
    {
        public float amplitude = 0.05f;
        public float spin = 35f;
        Vector3 origin;
        bool ready;

        void OnEnable()
        {
            origin = transform.localPosition;
            ready = true;
        }

        void Update()
        {
            if (!ready) return;
            transform.localPosition = origin + Vector3.up * (Mathf.Sin(Time.time * 2.1f) * amplitude);
            transform.Rotate(0f, spin * Time.deltaTime, 0f, Space.Self);
        }
    }
}
