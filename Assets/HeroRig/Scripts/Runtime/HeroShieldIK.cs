using UnityEngine;

namespace HeroRig
{
    /// <summary>
    /// Shield guard IK (guard mode). While the OneHandShield_Combat layer is in a Block state, the LEFT hand (shield hand)
    /// is pulled to a guard goal in front of the chest with Animator IK (the layer has IK Pass enabled).
    /// The goal is `target` if assigned, else `guardLocal` in the hero root's space scaled by humanScale / referenceHumanScale,
    /// so the shield sits out front at the same relative height on the male and the smaller female.
    /// The weight is deterministic (from state + normalized time), so it also works when the Animator is sampled in edit mode.
    /// </summary>
    [ExecuteAlways, RequireComponent(typeof(Animator)), DisallowMultipleComponent]
    public class HeroShieldIK : MonoBehaviour
    {
        public Animator animator;
        public string layerName = "OneHandShield_Combat";
        public string blockTag = "Block";
        public Transform target;
        public Vector3 guardLocal = new Vector3(0.02f, 1.12f, 0.42f);
        public float referenceHumanScale = 1f;
        [Range(0, 1)] public float positionWeight = 1f;
        [Range(0, 1)] public float rotationWeight = 0f;
        public Vector3 guardEuler = Vector3.zero;

        public float CurrentWeight { get; private set; }
        int _layer = -2;

        void OnEnable() { if (!animator) animator = GetComponent<Animator>(); _layer = -2; }

        public Vector3 GoalPosition()
        {
            if (target) return target.position;
            float k = animator && referenceHumanScale > 1e-4f ? animator.humanScale / referenceHumanScale : 1f;
            return transform.TransformPoint(guardLocal * k);
        }

        static float Smooth(float x) { x = Mathf.Clamp01(x); return x * x * (3f - 2f * x); }

        float Rule(AnimatorStateInfo s)
        {
            if (!s.IsTag(blockTag)) return 0f;
            if (s.IsName("BlockEnter")) return Smooth(s.normalizedTime);
            if (s.IsName("BlockHold")) return 1f;
            if (s.IsName("BlockExit")) return 1f - Smooth(s.normalizedTime);
            return 0f;
        }

        public float ComputeWeight()
        {
            if (!animator || !animator.runtimeAnimatorController) return 0f;
            if (_layer == -2) _layer = animator.GetLayerIndex(layerName);
            if (_layer < 0) return 0f;
            float w = Rule(animator.GetCurrentAnimatorStateInfo(_layer));
            if (animator.IsInTransition(_layer))
                w = Mathf.Lerp(w, Rule(animator.GetNextAnimatorStateInfo(_layer)), animator.GetAnimatorTransitionInfo(_layer).normalizedTime);
            return w;
        }

        void OnAnimatorIK(int layerIndex)
        {
            if (!animator) return;
            if (_layer == -2) _layer = animator.GetLayerIndex(layerName);
            if (layerIndex != _layer) return;
            float w = ComputeWeight();
            CurrentWeight = w;
            animator.SetIKPositionWeight(AvatarIKGoal.LeftHand, w * positionWeight);
            animator.SetIKRotationWeight(AvatarIKGoal.LeftHand, w * rotationWeight);
            if (w <= 0f) return;
            animator.SetIKPosition(AvatarIKGoal.LeftHand, GoalPosition());
            animator.SetIKRotation(AvatarIKGoal.LeftHand, transform.rotation * Quaternion.Euler(guardEuler));
        }

        void OnDrawGizmosSelected()
        {
            if (!animator) animator = GetComponent<Animator>();
            Gizmos.color = Color.cyan;
            Gizmos.DrawWireSphere(GoalPosition(), 0.05f);
        }
    }
}
