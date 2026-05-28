# WBS-063 IRF Targets

Status: approved for WBS-063 calibrated MVP IRF restrictions.

Source basis:
- BCB WP239 Section 4.1.1 says model IRFs are generally well behaved, show expected signs, and display hump-shaped paths.
- BCB WP239 Figure 3, PDF page 108 / printed page 107, reports impulse responses to a monetary policy shock.
- `docs/00b_modeling_decisions.md` MON-001 requires monetary-policy-shock IRFs to test sign, timing, magnitude, and benchmark.

Magnitude policy:
- Exact numeric magnitudes are not tabulated in WP239 Figure 3.
- Numeric magnitude is therefore deferred.
- WBS-063 tests only source-backed qualitative sign/timing and return-to-steady-state behavior.

## Target rows

```csv
target_id,target_type,shock_name,affected_variable,irf_field,expected_sign,sign_window_start,sign_window_end,expected_timing,numeric_magnitude,return_rule,return_horizon,benchmark_source,source_location,status,notes
IRF-MON-001,irf,eps_monetary,r_t,r_t_eps_monetary,positive,1,4,positive policy-rate response on impact and early horizons,deferred,abs_at_return_horizon_less_than_window_peak,20,BCB_WP239,Figure 3 monetary policy shock PDF page 108 printed page 107,approved_for_wbs063,Nominal interest rate panel is positive and returns toward steady state.
IRF-MON-002,irf,eps_monetary,c,c_eps_monetary,negative,1,4,private consumption falls after monetary tightening,deferred,abs_at_return_horizon_less_than_window_peak,20,BCB_WP239,Figure 3 monetary policy shock PDF page 108 printed page 107,approved_for_wbs063,Private consumption panel is negative and returns toward steady state.
IRF-MON-003,irf,eps_monetary,q,q_eps_monetary,negative,1,4,real exchange rate response is negative after tightening,deferred,abs_at_return_horizon_less_than_window_peak,20,BCB_WP239,Figure 3 monetary policy shock PDF page 108 printed page 107,approved_for_wbs063,Real exchange rate panel is below zero and moves back toward steady state.
IRF-MON-004,irf,eps_monetary,pi_a,pi_a_eps_monetary,negative,2,5,administered inflation falls after the policy shock with a delayed response,deferred,abs_at_return_horizon_less_than_window_peak,20,BCB_WP239,Figure 3 monetary policy shock PDF page 108 printed page 107,approved_for_wbs063,Administered inflation panel moves below zero after the shock; horizon 1 can be zero in the model.
IRF-MON-005,irf,eps_monetary,wn,wn_eps_monetary,negative,1,6,real wage falls after monetary tightening,deferred,abs_at_return_horizon_less_than_window_peak,20,BCB_WP239,Figure 3 monetary policy shock PDF page 108 printed page 107,approved_for_wbs063,Real wage panel is weakly negative and returns toward steady state.
```
