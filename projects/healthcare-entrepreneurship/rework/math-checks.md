# Machine-checked arithmetic

Every number below is one the book prints. `harness/tools/check_math.py` recomputes each with SymPy
during `build`, so a printed value that stops following from its stated inputs fails the build.

These blocks are not part of the book and never count against a chapter's word budget.

## Chapter 6 — ranking needs

```math-check
label: ch06 Worked Example - N1 weighted score
given: a=4, b=4, c=3, d=5
expr: 0.35*a+0.25*b+0.25*c+0.15*d
expect: 3.90 +- 0.001
```

```math-check
label: ch06 Worked Example - N2 weighted score
given: a=2, b=3, c=2, d=4
expr: 0.35*a+0.25*b+0.25*c+0.15*d
expect: 2.55 +- 0.001
```

```math-check
label: ch06 Worked Example - N3 weighted score
given: a=5, b=3, c=4, d=2
expr: 0.35*a+0.25*b+0.25*c+0.15*d
expect: 3.80 +- 0.001
```

```math-check
label: ch06 Worked Example - weights add to one
given: w1=0.35, w2=0.25, w3=0.25, w4=0.15
expr: w1+w2+w3+w4
expect: 1 +- 0.0001
```

```math-check
label: ch06 Q8 - weighted score
given: a=4, b=2, c=4, d=2
expr: 0.35*a+0.25*b+0.25*c+0.15*d
expect: 3.20 +- 0.001
```

## Chapter 8 — market size

```math-check
label: ch08 Worked Example - TAM
given: N=40000, f=4, p=400
expr: N*f*p
expect: exact 64000000
```

```math-check
label: ch08 Worked Example - SAM patients
given: N=40000, s=1/4
expr: N*s
expect: exact 10000
```

```math-check
label: ch08 Worked Example - SAM
given: N=10000, f=4, p=400
expr: N*f*p
expect: exact 16000000
```

```math-check
label: ch08 Worked Example - SOM patients
given: N=10000, s=6/100
expr: N*s
expect: exact 600
```

```math-check
label: ch08 Worked Example - SOM
given: N=600, f=4, p=400
expr: N*f*p
expect: exact 960000
```

```math-check
label: ch08 Worked Example - SOM visits a month
given: N=600, f=4
expr: N*f/12
expect: exact 200
```

```math-check
label: ch08 Q6 - market
given: N=20000, f=3, p=500
expr: N*f*p
expect: exact 30000000
```

```math-check
label: ch08 Q8 - SOM at 8 percent
given: N=10000, s=8/100, f=4, p=400
expr: N*s*f*p
expect: exact 1280000
```

## Chapter 9 — pilot measures

```math-check
label: ch09 Worked Example - completion rate
given: done=54, sched=60
expr: done/sched
expect: exact 9/10
```

```math-check
label: ch09 Worked Example - rejection rate
given: rej=3, recv=54
expr: rej/recv
expect: 0.056 +- 0.0005
```

```math-check
label: ch09 Q5 - completion rate
given: done=63, sched=72
expr: done/sched
expect: exact 7/8
```

## Chapter 11 — costs, break-even and funding

```math-check
label: ch11 Worked Example - variable cost per visit
given: t=40, c=25, h=35
expr: t+c+h
expect: exact 100
```

```math-check
label: ch11 Worked Example - monthly fixed cost
given: s=9000, sw=1500, ins=1500, rent=3000
expr: 2*s+sw+ins+rent
expect: exact 24000
```

```math-check
label: ch11 Worked Example - contribution margin
given: P=250, V=100
expr: P-V
expect: exact 150
```

```math-check
label: ch11 Worked Example - break-even visits
given: F=24000, P=250, V=100
expr: F/(P-V)
expect: exact 160
```

```math-check
label: ch11 Worked Example - profit at 200 visits
given: Q=200, cm=150, F=24000
expr: Q*cm-F
expect: exact 6000
```

```math-check
label: ch11 Worked Example - margin of safety
given: Q=200, QBE=160
expr: (Q-QBE)/Q
expect: exact 1/5
```

```math-check
label: ch11 Worked Example - monthly capacity
given: n=2, perday=10, days=22
expr: n*perday*days
expect: exact 440
```

```math-check
label: ch11 Table 11.1 - start-up total
given: boxes=4*3000, sw=20000, tr=8000, lic=15000, wc=3*24000
expr: boxes+sw+tr+lic+wc
expect: exact 127000
```

```math-check
label: ch11 Worked Example - monthly loss at 40 visits
given: Q=40, cm=150, F=24000
expr: F-Q*cm
expect: exact 18000
```

```math-check
label: ch11 Worked Example - cash after two months
given: wc=72000, loss=18000
expr: wc-2*loss
expect: exact 36000
```

```math-check
label: ch11 Worked Example - monthly loss at 80 visits
given: Q=80, cm=150, F=24000
expr: F-Q*cm
expect: exact 12000
```

```math-check
label: ch11 Worked Example - runway
given: cash=36000, burn=12000
expr: cash/burn
expect: exact 3
```

```math-check
label: ch11 Worked Example - contribution of 10 more visits
given: q=10, cm=150
expr: q*cm
expect: exact 1500
```

```math-check
label: ch11 In Practice - funding mix
given: own=30000, grant=50000, loan=47000
expr: own+grant+loan
expect: exact 127000
```

```math-check
label: ch11 Worked Example - round 1 post-money
given: pre=4000000, I=1000000
expr: pre+I
expect: exact 5000000
```

```math-check
label: ch11 Worked Example - round 1 angel share
given: I=1000000, post=5000000
expr: I/post
expect: exact 1/5
```

```math-check
label: ch11 Worked Example - founder after round 1
given: f=1/2, s=1/5
expr: f*(1-s)
expect: exact 2/5
```

```math-check
label: ch11 Worked Example - round 2 fund share
given: pre=12000000, I=3000000
expr: I/(pre+I)
expect: exact 1/5
```

```math-check
label: ch11 Worked Example - founder after round 2
given: f=2/5, s=1/5
expr: f*(1-s)
expect: exact 8/25
```

```math-check
label: ch11 Worked Example - angel after round 2
given: a=1/5, s=1/5
expr: a*(1-s)
expect: exact 4/25
```

```math-check
label: ch11 Worked Example - founder stake value before
given: f=1/2, v=4000000
expr: f*v
expect: exact 2000000
```

```math-check
label: ch11 Worked Example - founder stake value after
given: f=8/25, v=15000000
expr: f*v
expect: exact 4800000
```

```math-check
label: ch11 Worked Example - shares add to 100
given: a=32, b=32, c=16, d=20
expr: a+b+c+d
expect: exact 100
```

```math-check
label: ch11 Q3 - break-even scans
given: F=90000, P=900, V=300
expr: F/(P-V)
expect: exact 150
```

```math-check
label: ch11 Q4 - margin of safety
given: Q=250, QBE=150
expr: (Q-QBE)/Q
expect: exact 2/5
```

```math-check
label: ch11 Q5 - break-even at higher variable cost
given: F=24000, P=250, V=130
expr: F/(P-V)
expect: exact 200
```

```math-check
label: ch11 Q6 - runway
given: cash=60000, burn=15000
expr: cash/burn
expect: exact 4
```

```math-check
label: ch11 Q9 - investor share
given: pre=6000000, I=2000000
expr: I/(pre+I)
expect: exact 1/4
```

```math-check
label: ch11 Q10 - founder after dilution
given: f=3/5, s=1/4
expr: f*(1-s)
expect: exact 9/20
```

```math-check
label: ch11 E1 - break-even at 1,000 EGP
given: F=120000, P=1000, V=400
expr: F/(P-V)
expect: exact 200
```

```math-check
label: ch11 E1 - break-even at 1,200 EGP
given: F=120000, P=1200, V=400
expr: F/(P-V)
expect: exact 150
```
