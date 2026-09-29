# Machine-checked arithmetic

Every number below is one the book prints. `harness/tools/check_math.py` recomputes each with SymPy
during `build`, so a printed value that stops following from its stated inputs fails the build rather
than waiting for a reader to notice.

These blocks are not part of the book. They live here so that they never reach the assembled text and
never count against a chapter's word budget.

## Chapter 2 — one-compartment IV bolus

```math-check
label: ch02 Example 2.1 - K from two concentrations
given: C1=8.57, C2=1.11, t1=0, t2=12
expr: (log(C1) - log(C2))/(t2 - t1)
expect: 0.170 +- 0.001
```

```math-check
label: ch02 Example 2.1 - half-life from K
given: K=0.170
expr: log(2)/K
expect: 4.08 +- 0.01
```

```math-check
label: ch02 Example 2.1 - Vd from dose and back-extrapolated Cp0
given: D=300, Cp0=8.57
expr: D/Cp0
expect: 35.0 +- 0.1
```

```math-check
label: ch02 Example 2.1 - clearance is K times Vd
given: K=0.170, Vd=35.0
expr: K*Vd
expect: 5.95 +- 0.02
```

## Chapter 8 — repeated dosing

```math-check
label: ch08 Example 8.1 - fraction remaining over one interval of two half-lives
given: thalf=3, tau=6
expr: exp(-log(2)/thalf*tau)
expect: exact 1/4
```

```math-check
label: ch08 Example 8.1 - maximum amount at steady state
given: D=1000, f=Rational(1,4)
expr: D/(1 - f)
expect: 1333 +- 1
```

```math-check
label: ch08 Example 8.1 - minimum amount, and the peak-trough difference is one dose
given: D=1000, f=Rational(1,4), Dmax=D/(1-f)
expr: Dmax - Dmax*f
expect: exact 1000
```

```math-check
label: ch08 Example 8.1 - average amount at steady state
given: D=1000, K=log(2)/3, tau=6
expr: D/(K*tau)
expect: 721.3 +- 1
```

## Chapter 9 — non-compartmental analysis

```math-check
label: ch09 Example 9.1 - AUC tail extrapolated from the last concentration
given: Clast=0.40, lz=0.170
expr: Clast/lz
expect: 2.35 +- 0.01
```

```math-check
label: ch09 Example 9.1 - AUMC tail has two terms
given: Clast=0.40, lz=0.170, tlast=18
expr: tlast*Clast/lz + Clast/lz**2
expect: 56.19 +- 0.05
```

```math-check
label: ch09 Example 9.1 - mean residence time
given: AUMC=290.80, AUC=52.11
expr: AUMC/AUC
expect: 5.58 +- 0.01
```

```math-check
label: ch09 Example 9.1 - Vss is clearance times MRT
given: D=300, AUC=52.11, MRT=5.58
expr: D/AUC*MRT
expect: 32.1 +- 0.1
```

```math-check
label: ch09 Example 9.1 - the 6-12 h trapezoid overstates the true exponential area
given: Cp0=8.57, K=0.170, a=6, b=12
expr: Cp0/K*(exp(-K*a) - exp(-K*b))
expect: 11.6 +- 0.1
```

## Chapter 10 — saturable elimination

```math-check
label: ch10 Example 10.1 - steady state at 300 mg/day
given: Km=4, R=300, Vmax=500
expr: Km*R/(Vmax - R)
expect: exact 6
```

```math-check
label: ch10 Example 10.1 - steady state at 400 mg/day
given: Km=4, R=400, Vmax=500
expr: Km*R/(Vmax - R)
expect: exact 16
```

```math-check
label: ch10 Example 10.1 - instantaneous apparent half-life at 6 mg/L
given: Vd=45, Vmax=500, Km=4, C=6
expr: log(2)*Vd*(Km + C)/Vmax*24
expect: 15.0 +- 0.1
```

```math-check
label: ch10 Example 10.1 - integrated time to halve from 6 mg/L
given: Vd=45, Vmax=500, Km=4, C0=6
expr: (Vd/Vmax)*(Km*log(2) + C0/2)*24
expect: 12.5 +- 0.05
```

```math-check
label: ch10 Example 10.1 - integrated time to halve from 16 mg/L
given: Vd=45, Vmax=500, Km=4, C0=16
expr: (Vd/Vmax)*(Km*log(2) + C0/2)*24
expect: 23.3 +- 0.05
```

## Chapter 11 — metabolite kinetics

```math-check
label: ch11 Example 11.1 - time of the metabolite peak
given: K=0.2, Kmet=0.1
expr: log(Kmet/K)/(Kmet - K)
expect: 6.93 +- 0.01
```

```math-check
label: ch11 Example 11.1 - peak metabolite concentration
given: fm=Rational(2,5), K=Rational(1,5), D=500, Vdm=20, Kmet=Rational(1,10), tmax=log(Kmet/K)/(Kmet-K)
expr: fm*K*D/(Vdm*(Kmet - K))*(exp(-K*tmax) - exp(-Kmet*tmax))
expect: exact 5
```

```math-check
label: ch11 Example 11.1 - metabolite AUC by integration equals fm*D/Cl(m)
given: fm=Rational(2,5), K=Rational(1,5), D=500, Vdm=20, Kmet=Rational(1,10)
expr: fm*K*D/(Vdm*(Kmet - K))*(1/K - 1/Kmet) - fm*D/(Kmet*Vdm)
expect: exact 0
```

## Chapter 12 — pH partition

```math-check
label: ch12 Example 12.1 - Brodie ratio, stomach to blood
given: pKa=5.4, pHgut=3.4, pHblood=7.4
expr: (1 + 10**(pHblood - pKa))/(1 + 10**(pHgut - pKa))
expect: 100 +- 0.5
```

```math-check
label: ch12 Example 12.1 - Brodie ratio, intestine to blood
given: pKa=5.4, pHgut=6.4, pHblood=7.4
expr: (1 + 10**(pHblood - pKa))/(1 + 10**(pHgut - pKa))
expect: 9.2 +- 0.05
```

## Chapter 13 — bioavailability

```math-check
label: ch13 Example 13.1 - absolute bioavailability from dose-normalised areas
given: AUCoral=400, Doral=80, AUCiv=200, Div=10
expr: (AUCoral/Doral)/(AUCiv/Div)
expect: exact 1/4
```

```math-check
label: ch13 Example 13.1 - clearance from the IV arm
given: Div=10, AUCiv=0.200
expr: Div/AUCiv
expect: exact 50
```

```math-check
label: ch13 Example 13.1 - Cl/F from the oral arm agrees with Cl divided by F
given: Doral=80, AUCoral=0.400, Cl=50, F=Rational(1,4)
expr: Doral/AUCoral - Cl/F
expect: exact 0
```

```math-check
label: ch13 Example 13.1 - hepatic availability once fa is removed
given: F=0.25, fa=0.95, Fg=1
expr: F/(fa*Fg)
expect: 0.263 +- 0.002
```

```math-check
label: ch13 - the narrowed NTI range is the reciprocal pair 90 and 100/0.9
given: lo=90
expr: 10000/lo
expect: 111.11 +- 0.01
```

## Chapter 14 — dissolution

```math-check
label: ch14 Example 14.1 - average of the twelve units at stage S2
given: s1=492, s2=480
expr: (s1 + s2)/12
expect: exact 81
```

```math-check
label: ch14 Example 14.1 - the six S1 units average above Q+5 yet S1 still fails
given: s1=492
expr: s1/6
expect: exact 82
```

```math-check
label: ch14 - Noyes-Whitney dC/dt is the mass rate divided by the medium volume
given: rate=7.2, V=0.900
expr: rate/V
expect: 8.0 +- 0.01
```
