# Machine-checked arithmetic

Every number below is one the book prints. `harness/tools/check_math.py` recomputes each with SymPy
during `build`, so a printed value that stops following from its stated inputs fails the build.

These blocks are not part of the book and never count against a chapter's word budget.

## Chapter 2 — elasticity

```math-check
label: ch02 Worked Example - elasticity of the vitamin D test
given: P0=400, P1=500, Q0=300, Q1=270
expr: ((Q1-Q0)/Q0)/((P1-P0)/P0)
expect: exact -2/5
```

```math-check
label: ch02 Worked Example - revenue after the price rise
given: P1=500, Q1=270
expr: P1*Q1
expect: exact 135000
```

```math-check
label: ch02 Q8 - absolute elasticity
given: dq=5, dp=10
expr: dq/dp
expect: exact 1/2
```

## Chapter 5 — customer value

```math-check
label: ch05 Worked Example - value at laboratory A
given: b=80, money=30, travel=20, anx=5
expr: b-(money+travel+anx)
expect: exact 25
```

```math-check
label: ch05 Worked Example - value at laboratory B
given: b=75, money=35, travel=5, anx=5
expr: b-(money+travel+anx)
expect: exact 30
```

## Chapter 7 — pricing

```math-check
label: ch07 Worked Example - full cost per test
given: V=120, F=60000, Q=500
expr: V+F/Q
expect: exact 240
```

```math-check
label: ch07 Worked Example - cost-plus price at 25%
given: C=240, m=1/4
expr: C*(1+m)
expect: exact 300
```

```math-check
label: ch07 Worked Example - break-even volume
given: F=60000, P=300, V=120
expr: F/(P-V)
expect: 333.3 +- 0.05
```

```math-check
label: ch07 Q3 - cost-plus price at 20%
given: C=200, m=1/5
expr: C*(1+m)
expect: exact 240
```

```math-check
label: ch07 Q4 - break-even volume
given: F=40000, P=250, V=50
expr: F/(P-V)
expect: exact 200
```

```math-check
label: ch07 E1 - break-even at 900 EGP
given: F=90000, P=900, V=300
expr: F/(P-V)
expect: exact 150
```

```math-check
label: ch07 E1 - break-even at 1200 EGP
given: F=90000, P=1200, V=300
expr: F/(P-V)
expect: exact 100
```

## Chapter 10 — costs

```math-check
label: ch10 Worked Example - total cost of pathway A
given: dm=900, dn=100, ind=600
expr: dm+dn+ind
expect: exact 1600
```

```math-check
label: ch10 Worked Example - total cost of pathway B
given: dm=1500, dn=50, ind=250
expr: dm+dn+ind
expect: exact 1800
```

```math-check
label: ch10 Worked Example - incremental cost of B over A
given: A=1600, B=1800
expr: B-A
expect: exact 200
```

```math-check
label: ch10 Worked Example - difference from the hospital perspective
given: A=900, B=1500
expr: B-A
expect: exact 600
```

```math-check
label: ch10 Q6 - incremental cost
given: A=2000, B=2600
expr: B-A
expect: exact 600
```

## Chapter 11 — outcomes and ratios

```math-check
label: ch11 Worked Example - QALYs from full health
given: y=2, u=1, loss=1/4
expr: y*u*(1-loss)
expect: exact 3/2
```

```math-check
label: ch11 Worked Example - QALYs from a baseline of 0.8
given: y=2, u=4/5, loss=1/4
expr: y*u*(1-loss)
expect: exact 6/5
```

```math-check
label: ch11 Q2 - QALYs
given: y=4, u=1/2
expr: y*u
expect: exact 2
```

```math-check
label: ch11 Q6 - ICER per additional patient cured
given: CA=90000, CB=60000, EA=60, EB=50
expr: (CA-CB)/(EA-EB)
expect: exact 3000
```

```math-check
label: ch11 In Practice - CMA saving per course
given: A=250, B=350
expr: B-A
expect: exact 100
```

## Chapter 12 — applications

```math-check
label: ch12 Worked Example - micro-costed total
given: visits=8, vp=20, caps=28, cp=105/100, nights=7, np=50
expr: visits/2*vp + caps/4*cp + nights*np
expect: exact 43735/100
```

```math-check
label: ch12 Worked Example - hospital share of total
given: stay=350, total=43735/100
expr: stay/total
expect: 0.80 +- 0.005
```

```math-check
label: ch12 Worked Example - CMA saving, medicine 1 over 2
given: c1=18, c2=35
expr: c2-c1
expect: exact 17
```

```math-check
label: ch12 Worked Example - CER of medicine 1
given: c=18, e=25
expr: c/e
expect: exact 18/25
```

```math-check
label: ch12 Worked Example - CER of medicine 3
given: c=27, e=15
expr: c/e
expect: exact 9/5
```

```math-check
label: ch12 Worked Example - ICER of medicine 1 over 3
given: c1=18, c3=27, e1=25, e3=15
expr: (c1-c3)/(e1-e3)
expect: exact -9/10
```

```math-check
label: ch12 Worked Example - total cost of treatment A
given: a=10, b=5, c=30, d=15
expr: a+b+c+d
expect: exact 60
```

```math-check
label: ch12 Worked Example - total cost of treatment B
given: a=15, b=7, c=20, d=40
expr: a+b+c+d
expect: exact 82
```

```math-check
label: ch12 Worked Example - benefit-cost ratio of A
given: B=30, C=60
expr: B/C
expect: exact 1/2
```

```math-check
label: ch12 Worked Example - benefit-cost ratio of B
given: B=35, C=82
expr: B/C
expect: 0.43 +- 0.005
```

```math-check
label: ch12 Worked Example - incremental benefit-cost ratio
given: BA=30, BB=35, CA=60, CB=82
expr: (BB-BA)/(CB-CA)
expect: 0.23 +- 0.005
```

```math-check
label: ch12 Worked Example - net benefit of A
given: B=30, C=60
expr: B-C
expect: exact -30
```

```math-check
label: ch12 Worked Example - net benefit of B
given: B=35, C=82
expr: B-C
expect: exact -47
```

```math-check
label: ch12 Laboratory Example - CER of test A
given: c=60000, e=18
expr: c/e
expect: 3333 +- 0.5
```

```math-check
label: ch12 Laboratory Example - CER of test B
given: c=90000, e=24
expr: c/e
expect: exact 3750
```

```math-check
label: ch12 Laboratory Example - ICER of B over A
given: cA=60000, cB=90000, eA=18, eB=24
expr: (cB-cA)/(eB-eA)
expect: exact 5000
```

```math-check
label: ch12 Laboratory Example - ICER at the lower cost of B
given: cA=60000, cB=78000, eA=18, eB=24
expr: (cB-cA)/(eB-eA)
expect: exact 3000
```

```math-check
label: ch12 Q1 - cost of six visits
given: visits=6, vp=30
expr: visits/2*vp
expect: exact 90
```
