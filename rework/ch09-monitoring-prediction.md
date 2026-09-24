# Chapter 9: Monitoring, Prediction and Population Health

## Opening Case
Amal has been admitted to hospital with a urine infection. At 3 a.m., the ward computer shows an alert: "High risk of deterioration in the next 12 hours." Her heart rate has crept up and her blood pressure has drifted down. Her latest creatinine is higher than on admission.

The night nurse has seen three such alerts already tonight. Two were false alarms. She checks Amal herself. Amal is confused and her skin is cool. The nurse calls the doctor, who starts fluids and reviews her antibiotics. By morning, Amal is improving.

Prediction models promise earlier warning. But every alert takes time and attention. When does a warning help, and when does it become noise? This chapter looks at AI that watches patients over time, in hospital, at home and across whole populations.

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Explain how early-warning and prediction models work and why they create alarm burden.
2. [LO2] Interpret a prediction model's lead time against its false-alert rate.
3. [LO3] Describe AI applied to the electrocardiogram and the evidence from randomised trials.
4. [LO4] Describe closed-loop insulin delivery and who it is for.
5. [LO5] Evaluate a population-health AI claim using the lesson of Google Flu Trends.

> **Medical Background in 60 Seconds:** **Sepsis** is a life-threatening reaction to infection in which the body's response damages its own organs. Early signs include fast breathing, fast heart rate, low blood pressure and confusion. **Acute kidney injury** (AKI) is a rapid fall in kidney function over hours or days, often seen as a rising creatinine. Both are common in hospital, and both are easier to treat when caught early.

## 9.1 Early Warning: From Scores to Models
Hospitals have long used **early warning score**s. Nurses record vital signs, and each value earns points. The National Early Warning Score (NEWS2), used widely in the UK and elsewhere, adds points for breathing rate, oxygen level, blood pressure, pulse, consciousness and temperature [10]. A high total triggers a review. These are simple, transparent rule-based systems.

Machine-learning models go further. They use many more inputs, such as laboratory results, medicines and trends over time. They update continuously and aim to predict problems earlier.

The TREWS sepsis system was studied prospectively across five hospitals [1]. When clinicians confirmed its alert within three hours, patients had lower death rates than when alerts were not confirmed promptly. This was an observational study, not a randomised trial. Still, it is one of the stronger pieces of evidence for a hospital prediction tool.

Not all tools perform as claimed. A widely used commercial sepsis model, tested independently, missed two-thirds of sepsis cases and alerted on 18% of all patients admitted (Chapter 4) [2].

## 9.2 The Trade-Off: Lead Time Versus False Alerts
A prediction model can warn early or warn accurately. It is hard to do both. Warning earlier means predicting from weaker signals, which produces more false alarms.

A widely cited example is a model that predicted AKI in hospital patients [3]. It detected over half of all AKI episodes up to 48 hours before they happened, and 90% of the most severe episodes needing dialysis. But for every true alert, it produced about two false ones. The data came from US veterans' hospitals, and 93.6% of patients were men. The model's performance in women, and in other health systems, was uncertain.

These details matter in practice. On a 30-bed ward, a model with two false alerts per true alert might add many alerts a day. Each needs a nurse or doctor to check the patient. If staff lose trust, they begin to ignore alerts, just as with medication alerts (Chapter 7). This is **alarm fatigue**.

Good deployment asks practical questions. How many alerts per shift will this produce? Who responds, and with what action? What happens to other work while they respond?

## 9.3 AI and the Electrocardiogram
The **electrocardiogram** (ECG) records the heart's electrical activity. It is cheap, fast and available almost everywhere. Deep-learning models can find patterns in the ECG that people cannot see.

One model identified patients who had atrial fibrillation, an irregular heart rhythm linked to stroke, from an ECG recorded while their rhythm was normal [4]. Another model detects a weak heart pump, called low ejection fraction, from a standard ECG.

That second model was tested in a pragmatic randomised trial involving 120 primary-care teams and over 22,000 patients [5]. Teams that received the AI result diagnosed more cases of low ejection fraction than teams that did not. The absolute increase was modest: from 1.6% to 2.1% of patients. This is a realistic picture of benefit. An AI tool can help, but the effect in real care is often smaller than accuracy figures suggest.

![Figure 9.1 — Trend-based instability prediction](../images/image14.png)
*Figure 9.1 — A schematic arterial pressure trace. A prediction model flags a subtle trend before blood pressure falls clearly. Illustrative, not real patient data.*

## 9.4 Closed-Loop Insulin Delivery
People with **type 1 diabetes** make no insulin and must replace it every day. A **closed-loop system**, sometimes called an artificial pancreas, links three parts: a continuous glucose monitor, a control algorithm and an insulin pump (Figure 9.2). The monitor measures glucose every few minutes. The algorithm predicts where glucose is heading and adjusts insulin delivery automatically. Users still announce meals.

In a six-month randomised trial in people with type 1 diabetes, closed-loop control increased the time spent in the target glucose range from 59% to 71% of the day, compared with a pump and sensor without automation [6].

![Figure 9.2 — Closed-loop insulin delivery](figures/orig-image18.png)
*Figure 9.2 — A continuous glucose monitor feeds a dosing algorithm, which adjusts an insulin pump in a feedback loop. Illustrative.*

Amal has type 2 diabetes and does not use insulin. This tool is not designed for her current treatment. Recognising who a tool is for is part of using it safely.

## 9.5 Population Health
Public health watches whole communities rather than individual patients. AI supports surveillance by scanning news reports, social media and health records for signs of outbreaks. HealthMap, for example, automatically collects and maps online reports of infectious disease from around the world [7].

Google Flu Trends offers an important lesson. In 2009, researchers showed that the number of flu-related web searches tracked official influenza reports closely [8]. For a few years, it seemed a fast, cheap way to track flu. Then it failed. In the 2012–2013 season, it predicted more than double the proportion of flu-like doctor visits reported by the national disease agency [9].

Why? The model had learned from search terms that happened to rise in winter. People's search behaviour and the search engine itself changed over time. Media coverage of flu also drove searches from healthy people. The model had no link to the biology of influenza. This is distribution shift and shortcut learning at a population scale (Chapter 3).

> **Deeper Dive:** Suppose a ward sees 3 true deteriorations per day and a model catches 2 of them. If it produces 2 false alerts per true alert, staff receive 2 + 4 = 6 alerts per day. Only 1 in 3 is real: a PPV of 33%. Doubling the model's sensitivity by lowering the threshold might catch all 3 events, but could triple the false alerts. Whether that is worth it depends on staffing and what each alert costs in time.

> **Through Four Lenses**
> - **Medicine:** Physicians should know each alert's PPV and lead time. A deterioration alert should prompt a bedside review, not an automatic treatment, and the review should be documented.
> - **Pharmacy:** Pharmacists can act on kidney-injury alerts by reviewing doses of kidney-cleared drugs and stopping harmful combinations. Early medicine review can prevent the injury the model predicts.
> - **Physical Therapy:** Physiotherapists can use monitoring data to time mobilisation safely. Falling blood pressure or rising oxygen needs may mean delaying exercise, while stable trends support earlier movement.
> - **Health Sciences:** Public-health officers should compare digital signals with laboratory-confirmed data. Nutrition and laboratory staff contribute the measurements that give surveillance models real biological meaning.

> **Myth vs Evidence:** Myth: "Big data can replace traditional disease surveillance." Evidence: Google Flu Trends at first tracked influenza well [8], but later more than doubled the true rate [9]. Digital signals help most when combined with laboratory-confirmed surveillance.

> **Safety Alert:** An alert is a prompt to look at the patient, not a diagnosis. And no alert does not mean no problem. If a patient looks unwell, act, whatever the screen says.

## Key Takeaways
- Early-warning scores are rule-based; machine-learning models use more inputs and update continuously.
- Earlier warnings come with more false alerts; alarm burden decides whether a model helps.
- AI-ECG has randomised-trial evidence of modest real-world benefit.
- Closed-loop insulin delivery improves glucose control in type 1 diabetes.
- Population-level AI can fail through distribution shift, as Google Flu Trends showed.

## Self-Assessment
**Q1.** NEWS2 adds points for vital signs such as breathing rate and pulse. What kind of system is it? [LO1]
A) A deep-learning model
B) A rule-based early warning score
C) A large language model
D) A closed-loop controller

**Q2.** A kidney-injury model predicts events up to 48 hours early but produces two false alerts for every true one. What is the main practical concern? [LO2]
A) The model cannot detect severe cases.
B) Its training data were too large.
C) It uses creatinine.
D) Staff workload and alarm fatigue from frequent false alerts

**Q3.** The AKI model in Q2 was trained on a cohort that was 93.6% male. What should a hospital do before using it for all patients? [LO2]
A) Check its performance in women and in its own patient population
B) Use it only at night
C) Use it without changes because the cohort was large
D) Remove creatinine from the inputs

**Q4.** In a pragmatic randomised trial, AI-ECG results given to primary-care teams increased the diagnosis of low ejection fraction from 1.6% to 2.1%. What is the best interpretation? [LO3]
A) The AI replaced echocardiography.
B) The AI had no effect.
C) The AI produced a real but modest benefit in routine care.
D) The AI caused heart failure.

**Q5.** An AI model finds atrial fibrillation risk from an ECG recorded during normal rhythm. What does this show? [LO3]
A) The ECG was faulty.
B) Deep learning can find ECG patterns that people cannot see.
C) Atrial fibrillation is not linked to stroke.
D) The model uses the patient's age only.

**Q6.** Which patient is the intended user of a closed-loop insulin system? [LO4]
A) A person with type 1 diabetes who uses insulin
B) Amal, who has type 2 diabetes treated with tablets
C) A person with high blood pressure only
D) A patient with a knee injury

**Q7.** In a six-month randomised trial, what did closed-loop insulin delivery improve? [LO4]
A) Blood pressure
B) Kidney function
C) Weight loss only
D) Time spent in the target glucose range

**Q8.** Why did Google Flu Trends eventually fail? [LO5]
A) Nobody searched for flu any more.
B) Laboratory tests stopped.
C) Search behaviour and media coverage changed, so the search–flu link shifted.
D) The model was too small.

**Q9.** A new app claims to track an outbreak from social-media posts. What is the best way to evaluate it? [LO5]
A) Compare its signal over time with laboratory-confirmed surveillance data
B) Count the number of posts it reads
C) Trust it if it uses deep learning
D) Check whether it has a colourful map

**Q10.** A ward receives 6 deterioration alerts per day, of which 2 are true. What is the PPV of these alerts? [LO1]
A) 12%
B) 66%
C) 50%
D) 33%

**Case Question.** The ward manager wants to switch off the deterioration alerts because "most are false". Write a short reply that explains the trade-off and proposes one change that could keep the benefit while reducing the burden.

## Answers and Rationales
**Q1. B** — NEWS2 adds points using fixed rules [10]. A, C and D are different technologies.

**Q2. D** — Frequent false alerts create workload and fatigue [3]. A is false; it detected most severe cases. B and C are not concerns.

**Q3. A** — A model trained mostly on men must be checked in women and in the local population. B, C and D do not address the problem.

**Q4. C** — The trial showed a real but modest increase in diagnosis [5]. A, B and D misread the result.

**Q5. B** — The model detects subtle patterns invisible to readers [4]. A, C and D are false.

**Q6. A** — Closed-loop systems are designed for insulin users with type 1 diabetes [6]. B, C and D are not the intended users.

**Q7. D** — Time in range rose from 59% to 71% [6]. A, B and C were not the main outcome.

**Q8. C** — Changing behaviour and media shifted the relationship the model relied on [9]. A, B and D are wrong.

**Q9. A** — Digital signals should be validated against confirmed surveillance data. B, C and D do not test accuracy.

**Q10. D** — 2 ÷ 6 = 33%. A, B and C are wrong calculations.

**Case Question — model answer.** "I understand the frustration, because false alerts take time from other patients. But the alerts also catch real deterioration early, as with Amal last week. Switching them off loses that benefit. Instead, we could review the threshold with the informatics team, so that fewer low-value alerts fire. We could also agree a quick two-minute bedside check for each alert, and track how many alerts per shift we receive and how many are real."

## References
1. Adams R, Henry KE, Sridharan A, et al. Prospective, multi-site study of patient outcomes after implementation of the TREWS machine learning-based early warning system for sepsis. Nat Med. 2022;28(7):1455-1460. DOI: 10.1038/s41591-022-01894-0
2. Wong A, Otles E, Donnelly JP, et al. External validation of a widely implemented proprietary sepsis prediction model in hospitalized patients. JAMA Intern Med. 2021;181(8):1065-1070. DOI: 10.1001/jamainternmed.2021.2626
3. Tomašev N, Glorot X, Rae JW, et al. A clinically applicable approach to continuous prediction of future acute kidney injury. Nature. 2019;572(7767):116-119. DOI: 10.1038/s41586-019-1390-1
4. Attia ZI, Noseworthy PA, Lopez-Jimenez F, et al. An artificial intelligence-enabled ECG algorithm for the identification of patients with atrial fibrillation during sinus rhythm: a retrospective analysis of outcome prediction. Lancet. 2019;394(10201):861-867. DOI: 10.1016/S0140-6736(19)31721-0
5. Yao X, Rushlow DR, Inselman JW, et al. Artificial intelligence-enabled electrocardiograms for identification of patients with low ejection fraction: a pragmatic, randomized clinical trial. Nat Med. 2021;27(5):815-819. DOI: 10.1038/s41591-021-01335-4
6. Brown SA, Kovatchev BP, Raghinaru D, et al. Six-month randomized, multicenter trial of closed-loop control in type 1 diabetes. N Engl J Med. 2019;381(18):1707-1717. DOI: 10.1056/NEJMoa1907863
7. Freifeld CC, Mandl KD, Reis BY, Brownstein JS. HealthMap: global infectious disease monitoring through automated classification and visualization of Internet media reports. J Am Med Inform Assoc. 2008;15(2):150-157. DOI: 10.1197/jamia.M2544
8. Ginsberg J, Mohebbi MH, Patel RS, et al. Detecting influenza epidemics using search engine query data. Nature. 2009;457(7232):1012-1014. DOI: 10.1038/nature07634
9. Lazer D, Kennedy R, King G, Vespignani A. The parable of Google Flu: traps in big data analysis. Science. 2014;343(6176):1203-1205. DOI: 10.1126/science.1248506
10. Royal College of Physicians. National Early Warning Score (NEWS) 2: standardising the assessment of acute-illness severity in the NHS. London: RCP; 2017. https://www.rcp.ac.uk/improving-care/resources/national-early-warning-score-news-2/
