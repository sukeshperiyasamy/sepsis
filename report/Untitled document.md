COVER PAGE

SERS-BASED DETECTION OF BACTERIAL BIOMARKERS USING RAMAN SPECTROSCOPY FOR RAPID INFECTION SCREENING

Project Report submitted in partial fulfilment of the requirements for the award of the degree of Masters / Masters-Ph.D. in Medical Technologies

Submitted by  
Name of Student: ____________________  
Roll Number: ____________________

Under the supervision of  
Professor ____________________  
Professor ____________________

Indian Institute of Technology Jodhpur  
All India Institute of Medical Sciences Jodhpur  
Academic Year: ____________________


DECLARATION

I hereby declare that the work presented in this Project Report titled “SERS-Based Detection of Bacterial Biomarkers using Raman Spectroscopy for Rapid Infection Screening,” submitted to the Indian Institute of Technology Jodhpur and All India Institute of Medical Sciences Jodhpur in partial fulfilment of the requirements for the award of the degree of Masters / Masters-Ph.D. in Medical Technologies, is a bonafide record of the research work carried out under the supervision of Professor ____________________. The contents of this Project Report, in full or in part, have not been submitted to, and will not be submitted by me to, any other Institute or University in India or abroad for the award of any degree or diploma.

Signature: ____________________  
Name of Student: ____________________  
Roll Number: ____________________


CERTIFICATE

This is to certify that the Project Report titled “SERS-Based Detection of Bacterial Biomarkers using Raman Spectroscopy for Rapid Infection Screening,” submitted by ____________________ (Roll Number ____________________) to the Indian Institute of Technology Jodhpur and All India Institute of Medical Sciences Jodhpur for the award of the degree of Masters / Masters-Ph.D. in Medical Technologies, is a bonafide record of the research work done under my supervision. To the best of my knowledge, the contents of this report, in full or in part, have not been submitted to any other Institute or University for the award of any degree or diploma.

Signature: ____________________  
Name of Supervisor (1): ____________________

Signature: ____________________  
Name of Supervisor (2): ____________________


ABSTRACT

Sepsis is a time-critical clinical condition in which delayed diagnosis significantly increases morbidity, mortality, and treatment burden. Conventional diagnostics such as blood culture, PCR-based assays, and inflammatory biomarkers are useful in practice, but each method has limitations in speed, specificity, infrastructure, and cost. This project investigates a bacterial biomarker-focused Raman spectroscopy framework, with future translation toward Surface-Enhanced Raman Spectroscopy (SERS), for rapid infection screening.

The study targets three biologically relevant bacterial structural biomarkers: N-Acetylmuramic Acid (NAM) as a general bacterial indicator, Lipoteichoic Acid (LTA) as a Gram-positive indicator, and Lipopolysaccharide (LPS) as a Gram-negative indicator. Raman spectra were acquired under systematically varied experimental conditions, followed by a reproducible preprocessing pipeline including baseline correction, smoothing, normalization, and peak annotation. Spectral quality was quantified using signal-to-noise ratio (SNR) to identify optimal acquisition settings.

To improve molecular interpretability, Density Functional Theory (DFT)-based vibrational analysis was integrated with experimental observations. For large biomolecules such as LTA and LPS, fragment-based computational modeling was adopted to balance chemical relevance and computational feasibility. The completed work demonstrates methodological feasibility for biomarker-oriented optical screening and establishes an explainable framework combining experimental, computational, and literature-supported validation.

The current phase remains pre-clinical and does not claim diagnostic deployment. Ongoing work includes expanded LPS datasets, dilution-based studies, and reproducibility assessment. Future work will focus on SERS enhancement, AI-assisted classification, and clinical benchmarking against standard methods. Overall, this project provides a scientifically grounded foundation for future rapid, low-volume, and potentially portable infection-screening technologies.


TABLE OF CONTENTS

1. COMPREHENSIVE OVERVIEW OF THE STATE OF THE PROBLEM AND SOLUTIONS AVAILABLE ALONG WITH THEIR LIMITATIONS  
2. INTELLECTUAL PROPERTY (PATENT LANDSCAPING)  
3. OBJECTIVES AND METHODOLOGY  
4. DETAIL OF WORK DONE  
5. CONCLUSION  
6. NOVELTY  
7. POTENTIAL SOCIETAL AND MARKET IMPACT OF THE PROPOSED INNOVATION  
8. CHALLENGES OR RISK FACTORS ASSOCIATED WITH THE PROJECT  
9. ANY PATENT OR EQUIVALENT FILED  
10. RELEVANT REFERENCES


1. COMPREHENSIVE OVERVIEW OF THE STATE OF THE PROBLEM AND SOLUTIONS AVAILABLE ALONG WITH THEIR LIMITATIONS

1.1 Introduction

Sepsis is a life-threatening syndrome caused by a dysregulated host response to infection, resulting in organ dysfunction and, in severe cases, septic shock and death [1], [2]. It remains a major global health concern with high incidence across neonatal, pediatric, adult, and immunocompromised populations [3], [4]. A critical challenge in management is delayed recognition, since early symptoms are often non-specific and may overlap with non-infectious inflammatory states.

Timely initiation of appropriate antimicrobial therapy is associated with improved outcomes [5]. However, indiscriminate antibiotic use contributes to antimicrobial resistance, avoidable adverse effects, and increased healthcare expenditure. Therefore, there is a clinical need for rapid and interpretable diagnostic support that can guide early decision-making without compromising reliability.

Figure 1.1: Sepsis Progression and Clinical Urgency.

1.2 Need for Improved Diagnostics

An ideal infection-screening method should provide rapid turnaround, high sensitivity at low bacterial load, high specificity for bacterial infection, low sample-volume compatibility, minimal preparation steps, and practical portability. Existing methods satisfy only selected criteria, creating a translational gap between clinical urgency and diagnostic capability.

Figure 1.2: Ideal Diagnostic Requirements.

1.3 Existing Diagnostic Solutions and Their Limitations

1.3.1 Blood Culture (Current Gold Standard)

Blood culture is clinically accepted as the reference method because it confirms viable organisms and supports susceptibility testing. Its key limitations are long turnaround time, reduced yield after antibiotic exposure, and laboratory dependency [6], [7].

1.3.2 Molecular Diagnostics (PCR, qPCR, Multiplex Panels)

Molecular assays are faster than culture and can provide sensitive nucleic-acid detection. However, they are often target-restricted, expensive, and workflow-intensive. Detection may also include non-viable organisms.

1.3.3 Host Biomarker Tests (CRP, PCT, IL-6, TNF-alpha)

Host biomarkers are useful supportive indicators and are widely available, but they are indirect signals of inflammation and may be elevated in non-infectious conditions, reducing pathogen specificity.

1.3.4 Raman Spectroscopy and Surface-Enhanced Raman Spectroscopy (SERS)

Raman spectroscopy is a label-free optical technique that captures molecular fingerprints through vibrational signatures. SERS can substantially amplify weak Raman signals via plasmonic substrates. Current translational challenges include substrate variability, biological matrix complexity, and the requirement for robust preprocessing and validation.

Table 1.1: Comparative Analysis of Existing Diagnostic Methods.

Method	Speed	Direct Bacterial Evidence	Gram Information	Portability	Major Limitation  
Blood Culture	Slow	Yes	Yes	Low	Long turnaround time  
PCR	Moderate	Yes (DNA)	Yes	Low to Moderate	High cost and target restriction  
CRP/PCT	Fast	No	No	Moderate	Limited specificity  
Raman/SERS	Fast	Yes	Potential	High (future)	Needs clinical validation

Figure 1.3: Diagnostic Timeline Comparison.

1.4 Strategic Biomarker-Based Detection Approach

To reduce early-stage complexity, this project adopts a biomarker-first strategy based on bacterial structural targets: NAM (general marker), LTA (Gram-positive marker), and LPS (Gram-negative marker). This approach supports biologically interpretable screening logic while enabling staged translational development.

Figure 1.4: Biomarker Logic Diagram.

1.5 Research Gap

No current mainstream platform simultaneously offers rapid turnaround, low-volume compatibility, direct structural bacterial evidence, explainable molecular interpretation, and realistic portability potential. This unmet need motivates the present work.

1.6 Proposed Research Direction

The project follows a staged model: controlled Raman validation, expanded reproducibility and sensitivity studies, SERS integration, AI-assisted interpretation, and future clinical benchmarking.

Figure 1.5: Thesis Roadmap.

1.7 Significance of the Present Work

This work contributes a foundational and explainable framework combining biomarker biology, Raman spectroscopy, and computational validation. It establishes scientific readiness for future portable infection-screening development.

1.8 Chapter Summary

This chapter established the clinical context, limitations of current diagnostics, and the rationale for a biomarker-focused Raman/SERS translational pathway.


2. INTELLECTUAL PROPERTY (PATENT LANDSCAPING)

2.1 Introduction

Intellectual property analysis was conducted to evaluate novelty opportunities, crowded domains, and strategic differentiation for Raman/SERS-based infection screening.

2.2 Objectives of Patent Landscaping

The chapter addresses five questions: current technology landscape, dense patent areas, remaining white spaces, potentially patentable elements of this work, and future differentiation strategy.

2.3 Major Patent Domains Relevant to the Project

Table 2.1: Patent Domain Relevance Matrix.

Domain	Typical Patent Focus	Relevance  
Sepsis diagnostics	Biomarker kits, risk scoring	High  
Molecular diagnostics	PCR cartridges, nucleic acid panels	High  
Raman systems	Spectral devices, libraries	High  
SERS materials	Nanostructures, hotspot architectures	High  
AI diagnostics	Classification algorithms	Medium to High  
Portable devices	Handheld analyzers	High  
Microfluidics	Sample-preparation cartridges	Future relevance  
Neonatal diagnostics	Low-volume workflows	Strategic niche

2.4 Existing Patent Trends in Sepsis Diagnostics

Most filings are concentrated in host biomarker diagnostics, molecular pathogen detection platforms, and culture-automation improvements. While valuable, these categories do not fully solve the rapid, low-volume, direct structural evidence gap.

Figure 2.1: Existing Sepsis Patent Categories.

2.5 Existing Patent Trends in Raman and SERS Diagnostics

Raman patents commonly focus on laboratory classification workflows. SERS patents are heavily concentrated on substrate engineering and enhancement architecture. Portable optical device patents exist but are often not infection-specific.

2.6 White-Space Opportunities

Key opportunities include structural biomarker panels for rapid screening, DFT-supported explainable diagnostics, neonatal low-volume testing workflows, and integrated portable reader-cartridge systems.

Figure 2.2: White-Space Opportunity Matrix.

2.7 Potential Patentable Outputs from This Thesis

Table 2.2: Potential IP Portfolio from Thesis.

Category	Potential Output  
Method	Raman/SERS biomarker detection workflow and Gram-oriented logic  
Device	Portable optical reader and low-volume cartridge  
Material	Reproducible Ag/Au SERS substrate and functionalized surface  
Software	Preprocessing engine, classifier, and explainability module

2.8 Competitive Comparison with Existing Technologies

This approach is positioned as a rapid and interpretable screening layer that complements existing diagnostic pathways.

Figure 2.3: Competitive Positioning Map.

2.9 Freedom-to-Operate Considerations

This chapter is strategic and does not constitute a legal FTO opinion. Formal patent counsel review is required before commercialization.

2.10 Current Status vs Future IP Readiness

Current outputs support conceptual differentiation. Stronger filings are expected after expanded performance data, prototype stabilization, and comparative validation.

2.11 Strategic Conclusion

The landscape is active but fragmented. The project appears to occupy a potentially differentiated white-space in explainable, low-volume, and portable bacterial screening.

2.12 Chapter Summary

This chapter summarized relevant patent domains, existing trends, and practical future IP pathways.


3. OBJECTIVES AND METHODOLOGY

3.1 Introduction

This chapter defines project objectives and the methodological framework used to establish biomarker-focused Raman feasibility with future SERS translation.

3.2 Research Objectives

Objective 1: Detect Raman signatures of NAM, LTA, and LPS under optimized acquisition conditions.  
Objective 2: Validate spectral interpretation using DFT-based vibrational analysis.  
Objective 3: Develop a reproducible preprocessing and analysis pipeline.  
Objective 4: Define a translational pathway toward a portable SERS screening platform.

Table 3.1: Objectives, Methods, and Expected Outputs.

Objective	Method	Output  
Biomarker detection	Raman experiments	Spectral signature library  
Computational validation	DFT simulations	Peak assignments  
Data pipeline	Signal processing	Reproducible spectra  
Translation planning	Concept design	Future prototype roadmap

3.3 Overall Methodological Framework

The workflow was designed as a phased process: biomarker selection, controlled sample preparation, Raman acquisition, preprocessing, peak analysis, DFT validation, and translational planning.

Figure 3.1: Full Experimental Workflow.

3.4 Phase I - Current Experimental Methodology

3.4.1 Biomarker Selection Strategy  
Biomarkers were selected based on biological relevance, literature support, and interpretability.

3.4.2 Materials and Sample Preparation  
Analytical-grade biomolecular standards were used to establish controlled reference spectra.

Table 3.2: Experimental Materials Summary.

Material	Purpose	Status  
NAM	General biomarker study	Completed  
LTA	Gram-positive biomarker	Completed  
LPS	Gram-negative biomarker	Ongoing  
Rhodamine B	Reference workflow validation	Completed

3.4.3 Raman Instrumentation  
Acquisition variables included laser power, integration time, accumulations, spectral range, and replicate scans.

Table 3.3: Instrument and Acquisition Parameters.  
(Insert instrument-specific values.)

3.4.4 Experimental Design and Optimization  
Systematic condition matrices were used to identify robust settings for quality and reproducibility.

3.4.5 Raw Data Preprocessing Pipeline  
Preprocessing included dark correction (where applicable), ALS baseline correction, Savitzky-Golay smoothing, normalization, and peak annotation.

3.4.6 Signal-to-Noise Ratio (SNR) Analysis  
Equation (3.1): SNR = Isignal / sigmanoise

3.5 Computational Methodology (DFT)

3.5.1 Software Environment  
DFT and molecular visualization tools were used for vibrational interpretation.

3.5.2 General Workflow  
Structure preparation, optimization, frequency calculation, scaling, and spectrum comparison were performed.

3.5.3 Typical Computational Settings  
Representative functionals and basis sets were selected according to standard computational spectroscopy practice.

3.5.4 Frequency Scaling  
Equation (3.2): nuscaled = nucalc x f

3.5.5 Comparison Metrics  
Peak match count, mean absolute deviation, and RMSE were used to evaluate agreement quality.

3.5.6 Component-Based Modeling for Large Molecules  
Fragment-based modeling was used for large biomolecules to preserve interpretability while maintaining feasibility.

3.6 Validation Framework

A three-layer framework was adopted: experimental evidence, DFT-supported interpretation, and literature consistency.

3.7 Current Status of Method Execution

Completed: NAM and LTA Raman analysis, preprocessing workflow, and DFT framework.  
Ongoing: LPS expansion and reproducibility studies.  
Future: SERS integration, AI modeling, and clinical benchmarking.

3.8 Methodological Strengths

The methodology is structured, reproducible, and explainable, with clear progression from feasibility to translational readiness.

3.9 Chapter Summary

This chapter presented objectives, workflow design, computational support, and implementation status.


4. DETAIL OF WORK DONE

4.1 Introduction

This chapter presents the executed experimental and computational work, including optimization, validation, and interpretation outcomes.

4.2 Research Execution Summary

Table 4.1: Work Status Summary.

Activity	Status  
NAM Raman	Completed  
NAM DFT	Completed  
LTA Raman	Completed  
LTA component modeling	Completed  
LPS study	Ongoing  
Dilution studies	Ongoing  
Portable prototype	Future

4.3 Stage I - Workflow Validation Using Rhodamine B

Rhodamine B was used as a reference molecule to validate the analysis pipeline before biomarker-specific interpretation.

Figure 4.1: Rhodamine B Molecular Structure.  
Figure 4.2: Rhodamine B Experimental vs Simulated Spectrum.

4.4 Stage II - Experimental Raman Study of NAM

NAM spectra were collected across multiple settings, preprocessed, and ranked using SNR to select optimal conditions.

Table 4.2: NAM Experimental Conditions.  
Figure 4.3: Raw vs Processed NAM Spectrum.  
Figure 4.4: NAM SNR Ranking Chart.  
Figure 4.5: NAM Optimization Heatmap.  
Figure 4.6: Best NAM Spectrum with Peak Labels.  
Table 4.3: NAM Experimental Peak Table.

4.5 Stage III - DFT Validation of NAM

DFT-generated frequencies were compared with experimental peaks to support assignment confidence.

Figure 4.7: NAM Experimental vs DFT Overlay.  
Table 4.4: NAM Validation Table.

4.6 Stage IV - Experimental Raman Study of LTA

LTA analysis showed broad and complex spectral bands, requiring region-focused interpretation.

Figure 4.8: Simplified LTA Structure.  
Figure 4.9: LTA Parameter Comparison Spectra.  
Figure 4.10: Best LTA Spectrum with Region Labels.  
Table 4.5: LTA Region Interpretation Table.

4.7 Stage V - Component-Based Modeling of LTA

Representative LTA fragments were modeled to map major structural contributions with computational efficiency.

Figure 4.11: LTA Fragment Strategy Diagram.  
Figure 4.12: Simulated Component Spectra.

4.8 Stage VI - LPS Work Status

LPS experimental and computational workflows are underway, with focus on robust signal extraction and interpretability.

Figure 4.13: Simplified LPS Structure.  
Figure 4.14: Planned LPS Validation Workflow.

4.9 Unified Validation Framework Developed During Thesis

A common validation model integrating experiment, computation, and literature evidence was established for all biomarkers.

4.10 Major Quantitative Findings

Table 4.6: Thesis Key Metrics Summary.  
(Insert final measured values.)

4.11 Key Learnings

Optimization of acquisition parameters, standardized preprocessing, and theory-assisted assignment are central to reliable Raman biomarker interpretation.

4.12 Limitations of Current Work

Current limitations include pure-standard datasets, incomplete LPS expansion, and absence of clinical sensitivity/specificity validation.

4.13 Chapter Conclusion

The completed work provides a scientifically credible foundation for future SERS-enabled translational development.


5. CONCLUSION

5.1 Introduction

This chapter summarizes the principal outcomes, contribution, and future direction of the project.

5.2 Summary of Major Contributions

The project established biomarker-focused Raman feasibility, optimized acquisition and preprocessing strategy, DFT-supported interpretation, and a translational roadmap toward portable screening.

5.3 Scientific Conclusions

The study demonstrates that selected bacterial structural biomarkers can be characterized under optimized Raman conditions and interpreted with improved confidence using DFT-assisted analysis.

5.4 Clinical and Technological Relevance

Although pre-clinical, the framework has potential relevance for rapid triage support in high-acuity and low-resource care settings, subject to formal validation.

5.5 Limitations of the Present Thesis

Clinical matrix validation, larger reproducibility datasets, and SERS/AI integration remain future priorities.

5.6 Future Scope

Future work includes LPS completion, dilution-based semi-quantitative studies, reproducible SERS substrate development, AI model training, and clinical benchmarking.

5.7 Final Conclusion

This thesis provides a rigorous and explainable foundation for developing future rapid infection-screening systems based on Raman/SERS technologies.

5.8 Chapter Summary

The chapter consolidated achievements, limitations, and a practical translational path forward.


6. NOVELTY

6.1 Introduction

Novelty in this work arises from integrated design rather than a single isolated contribution.

6.2 Core Novelty Elements

6.2.1 Structural biomarker-first detection strategy.  
6.2.2 Label-free Raman fingerprinting framework.  
6.2.3 DFT-supported explainable interpretation.  
6.2.4 Fragment-based modeling for large biomolecules.  
6.2.5 Built-in translational pathway toward SERS-enabled portable screening.

6.3 Novelty Compared with Existing Technologies

Table 6.1: Technology Comparison Matrix.  
(Insert final comparative data in tabular form.)

6.4 Novelty Relative to Published Research

The thesis contributes systems-level integration across biomarker logic, spectroscopy, computational validation, and translational planning.

6.5 Novelty in Methodological Design

A multi-layer validation framework and staged progression were used to improve robustness and reduce translational risk.

6.6 Novelty in Market Positioning

The approach aims for differentiated positioning through speed, interpretability, and future portability.

6.7 Completed vs Future Novel Scope

Current novelty is methodological and foundational; future novelty depends on validated SERS performance and clinical utility outcomes.

6.8 Unique Value Proposition

Rapid, explainable, biomarker-based optical bacterial screening with future low-volume and portable deployment potential.

6.9 Chapter Conclusion

The novelty is academically defensible and aligned with translational healthcare needs.

6.10 Chapter Summary

This chapter defined and contextualized the novelty contribution of the project.


7. POTENTIAL SOCIETAL AND MARKET IMPACT OF THE PROPOSED INNOVATION

7.1 Introduction

This chapter evaluates potential impact across patient care, public health, healthcare systems, and market deployment.

7.2 Potential Societal Impact - Clinical Care

A rapid screening layer may reduce diagnostic uncertainty and support earlier decisions in acute care, particularly for vulnerable groups.

7.3 Public Health Impact

Improved diagnostic support can strengthen antimicrobial stewardship and contribute indirectly to AMR mitigation.

7.4 Healthcare System Impact

Potential effects include improved triage efficiency, reduced avoidable investigations, and better resource utilization.

7.5 Educational and Research Impact

The project supports interdisciplinary training in spectroscopy, computational analysis, and translational innovation.

7.6 Market Opportunity

Table 7.1: Target Market Segments.

Segment	Potential Need  
Tertiary hospitals	Rapid infection support  
NICUs/PICUs	Low-volume screening  
Emergency departments	Fast triage  
Diagnostic networks	Advanced rapid testing  
Rural clinics	Portable screening  
Public health programs	Scalable deployment  
Global health organizations	Low-resource diagnostics

7.7 Competitive Market Position

The technology is positioned as a complementary rapid screening layer, not a replacement for gold-standard diagnostics.

7.8 Current Impact vs Future Impact

Current impact is scientific and methodological; large-scale impact depends on prototype validation and clinical adoption.

7.9 Measurable Impact Indicators

Table 7.2: Future Impact Metrics.

Metric	Example  
Time-to-result	Minutes versus hours/days  
Sensitivity/Specificity	Against reference standards  
Cost per test	Compared with current options  
Adoption rate	Number of deployment sites  
Antibiotic decision support	Change in prescribing behavior  
Sample volume	Micro-volume compatibility

7.10 Chapter Conclusion

The project has meaningful societal and market potential, contingent on phased evidence generation.

7.11 Chapter Summary

This chapter outlined impact pathways and measurable outcomes for future translational stages.


8. CHALLENGES OR RISK FACTORS ASSOCIATED WITH THE PROJECT

8.1 Introduction

This chapter identifies major risks affecting technical development, clinical translation, and eventual adoption.

8.2 Risk Assessment Framework

Risks are prioritized by probability and impact to guide mitigation planning.

8.3 Technical Risks

Weak signal at low concentrations, baseline/noise artifacts, and substrate variability are primary technical risks.

Table 8.1: Technical Risks and Mitigation.

Risk	Impact	Mitigation  
Weak signal	Missed detection	Optimization and SERS enhancement  
Noise artifacts	Misinterpretation	Standardized preprocessing and QC  
Substrate variability	Poor reproducibility	Batch control and characterization

8.4 Scientific Risks

Specificity limitations and interpretation in complex clinical matrices require cautious, multi-marker validation.

8.5 Experimental and Data Risks

Small datasets, cross-day variation, and quantification uncertainty require expanded studies and standardized protocols.

Table 8.2: Data Risks and Controls.

8.6 Clinical Translation Risks

Benchmarking against standard methods and workflow integration are essential for clinician acceptance.

8.7 Regulatory and Ethical Risks

Regulatory compliance and data governance are critical for clinical deployment readiness.

8.8 Manufacturing and Commercial Risks

Scale-up cost, competition, and procurement economics may affect adoption.

Table 8.3: Commercial Risks and Responses.

8.9 Project-Specific Critical Success Factors

Critical factors include reproducible spectra, robust discrimination logic, validated performance, usability, and scalable implementation.

8.10 Current Status vs Future Risk Exposure

Current risks are manageable at research scale; regulatory and commercialization risks increase in later stages.

8.11 Overall Risk Assessment

The project carries moderate translational risk typical of early biomedical technologies.

8.12 Chapter Conclusion

Risks are significant but addressable through systematic, staged, evidence-driven progression.

8.13 Chapter Summary

This chapter provided a structured risk map and mitigation pathway for future development.


9. ANY PATENT OR EQUIVALENT FILED

9.1 Introduction

This chapter presents current IP status and future protection opportunities arising from the project.

9.2 Current Filing Status

As of the present submission stage, no formal patent filing is claimed unless officially documented through institutional channels.

9.3 Why Filing May Be Deferred

Deferral may be strategic when stronger claims are expected after expanded data and prototype maturity.

9.4 Potentially Patentable Outcomes Identified

Potential assets include method, device, material, and software innovations.

9.5 Alignment with Thesis Work

Current outputs support concept-level IP potential and can be strengthened through further validation.

9.6 Suggested Future Patent Titles

Potential titles may be finalized after prior-art mapping and institutional IP consultation.

9.7 Competitive Positioning of Future IP

Differentiation is expected in explainable structural biomarker screening and integrated translational architecture.

9.8 Equivalent Non-Patent Intellectual Property

Non-patent assets include datasets, workflows, SOPs, code, and technical know-how.

9.9 Recommended Future IP Roadmap

Table 9.1: Future IP Roadmap.

Stage	Recommended Action  
Current stage	Consolidate evidence and claim mapping  
Expanded results	Prepare invention disclosure  
Prototype	File provisional patent  
Advanced validation	File complete patent/PCT  
Commercialization	License/startup/partnership model

9.10 Risks in Future IP Strategy

Prior-art overlap, premature public disclosure, weak claims, and ownership ambiguity are key risks.

9.11 Strategic Conclusion

The project supports a platform-oriented IP strategy with potential for multiple complementary filings.

9.12 Chapter Summary

This chapter clarified current IP status and practical future filing directions.


10. RELEVANT REFERENCES

10.1 Introduction

References are listed in IEEE citation order and should match in-text citation sequence.

10.2 Recommended Citation Standard

Use numbered bracket citations in text, for example [1], [2], [3], and list entries in order of first appearance.

10.3 Core References

[1] M. Singer et al., “The Third International Consensus Definitions for Sepsis and Septic Shock (Sepsis-3),” JAMA, vol. 315, no. 8, pp. 801-810, 2016.  
[2] A. Kumar et al., “Duration of hypotension before initiation of effective antimicrobial therapy is the critical determinant of survival in human septic shock,” Critical Care Medicine, vol. 34, no. 6, pp. 1589-1596, 2006.  
[3] World Health Organization, “Sepsis: Global Health Resources and Reports.”  
[4] K. E. Rudd et al., “Global, regional, and national sepsis incidence and mortality,” The Lancet, 2020.  
[5] M. Cecconi et al., “Sepsis and septic shock,” The Lancet, vol. 392, pp. 75-87, 2018.  
[6] H. J. Butler et al., “Using Raman spectroscopy to characterize biological materials,” Nature Protocols, 2016.  
[7] K. Kong et al., “Raman spectroscopy for medical diagnostics,” Journal of Biophotonics, 2015.  
[8] B. Sharma et al., “SERS: materials, applications, and the future,” Materials Today, 2012.  
[9] S. Schlucker, “Surface-enhanced Raman spectroscopy: concepts and applications,” Angewandte Chemie International Edition, 2014.  
[10] M. J. Frisch et al., Gaussian Software Documentation, Gaussian Inc.  
[11] A. D. Becke, “Density-functional thermochemistry. III. The role of exact exchange,” Journal of Chemical Physics, 1993.  
[12] C. Lee, W. Yang, and R. G. Parr, “Development of the Colle-Salvetti correlation-energy formula into a functional of the electron density,” Physical Review B, 1988.  
[13] A. P. Scott and L. Radom, “Harmonic vibrational frequencies: scale factors for HF and DFT methods,” Journal of Physical Chemistry, 1996.

10.4 Thesis-Specific References Pending Finalization

Table 10.1: Thesis-Specific References to Finalize.

Category	Required Sources  
NAM Raman studies	Final papers used in this project  
LTA Raman studies	Final papers used in this project  
LPS Raman studies	Final papers used in this project  
Rhodamine B benchmarking	Final validation references  
Functional group assignments	Standard spectroscopy handbooks  
Preprocessing methods	ALS and Savitzky-Golay method papers

10.5 Reference Quality Checklist

All in-text citations must appear in the reference list. All listed references must be cited. DOI information should be included where available. Formatting must remain consistent with IEEE style throughout.
