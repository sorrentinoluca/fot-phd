# **Representing Time Series as Structured Programs for LLM Reasoning** 

**Jaeho Kim**<sup>**1***</sup> **, Changjun Oh**<sup>**1***</sup> **, Seokhyun Lee**<sup>**1**</sup> **, Irina Rish**<sup>**2**</sup> **, Changhee Lee**<sup>**1**†</sup> 1Korea University, 2Mila, University of Montreal 

## **Abstract** 

Large language models (LLMs) have demonstrated strong reasoning and instructionfollowing capabilities, making them potentially powerful tools for time-series analysis. However, time series lie outside their native textual modality, raising a fundamental question: _how should time series be represented so that LLMs can reason about them effectively?_ Existing work typically serializes raw numerical sequences or fine-tunes pre-trained LLMs on time-series data. These approaches place the burden of extracting temporal structure directly on the LLM, creating a modality mismatch that often degrades performance on long sequences and introduces substantial computational overhead. In this work, we introduce Time-Seriesto-Structured-Program representation (T2SP), a deterministic, training-free method that represents a time series as a _structured symbolic program_ . T2SP decomposes time series into trends, periods, and salient events, expressing them in a _program-friendly_ format aligned with the textual and code-like modalities on which LLMs are natively trained. By shifting temporal-structure extraction from the model to the representation itself, T2SP enables off-theshelf LLMs to leverage their existing reasoning capabilities for time-series understanding. We evaluate T2SP on three reasoning tasks – editing, captioning, and question answering – where it consistently improves performance, reduces reasoning time, and lowers failure rates compared with raw-string representations. Our results demonstrate that T2SP provides an effective interface between time series and LLMs. 

## **1 Introduction** 

Large language models (LLMs) have achieved strong success across diverse domains such as mathematics (Hendrycks et al., 2021), coding (Chen et al., 2021), and reasoning (Lu et al., 

> *Equal Contribution. 

> †Corresponding author. 


![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0001-09.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0001-10.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0001-11.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0001-12.png)


Figure 1: **Representations matter for LLM-based timeseries reasoning.** (A) Raw numerical sequences are dense and heterogeneous, forcing LLMs to infer the temporal structure value by value. (B) LLMs are pretrained on a vast corpus of natural language texts and code representations (Touvron et al., 2023), making them well-suited for reasoning over symbolic and functional forms (Gao et al., 2023; Chen et al., 2023). 

2024), with their ability to follow instructions and reason over textual information increasingly approaching human-level performance (Phan et al., 2025). Building on these successes, a growing line of work has begun to apply LLM capabilities to time-series analysis (Jin et al., 2024), asking LLMs to interpret, edit, and reason about temporal data, beyond classical classification and forecasting. However, LLMs that excel elsewhere have been shown to struggle with extracting meaningful structures from raw time series (Merrill et al., 2024), and consequently fail on seemingly simple time-series analysis tasks. We argue that this gap arises not from a deficiency of the model, but from a representation mismatch (shown in Figure 1). 

Yet the dominant response in the literature has focused on the _model side_ of the interface, taking three mainstream directions. The first and most direct method is to feed the _raw time series as a string_ , requiring the LLM to interpret raw values directly. Although this preserves the full fidelity of the sequence, this approach breaks down as sequence length grows (Fons et al., 2024), and 

1 

LLMs are known to struggle with raw numerical inputs (Zhou et al., 2025). A second line of work converts time series into visual plots and uses vision-language models (VLMs) for analysis. While vision-based models are effective at capturing the holistic shape of a series in a form readable to humans, they struggle to capture structural components such as periodicity or localized events, limiting their applicability to tasks that require a fine-grained understanding (Sen et al., 2025). A third approach is to fully or partially fine-tune the LLM on time-series or domain-specific representations (Wang et al., 2025). Unfortunately, such methods are computationally expensive and not applicable to the strongest closed-source LLMs accessible only via APIs, limiting their scalability. These approaches share a commonality: _they push the burden of time-series understanding onto the model_ – asking the model to read numerical sequences, switch modalities, or even retrain the model. We take the opposite view. _We argue that the model is already highly capable_ ; what is needed is a representation that (i) preserves the informative structure of time series with sufficient fidelity, and (ii) exposes that structure in a symbolic form the LLM can natively parse and reason over. 

How, then, _should time series be represented to satisfy both criteria?_ Our answer is that time series should be re-expressed in a _program-friendly_ and _structured_ format that LLMs can already reason over effectively. Whereas a list of raw numbers forces the model to understand the temporal structure value by value, a structural representation of time series aligns with the symbolic and code-like expressions LLMs handle fluently (Gao et al., 2023; Achiam et al., 2023). Motivated by this perspective, we introduce the Time-Series-to-StructuredProgram representation (T2SP), a novel time-series representation method for interfacing time series with LLMs. T2SP _deterministically_ decomposes a raw series into components of trend, periodic, event, and residual components, and expresses them as a structured program using program-like syntax that is readable by both humans and LLMs. Our contributions are as follows: 

- We propose T2SP, a time-series representation with a structured and program-like syntax that aligns with the modalities on which LLMs were natively trained, enabling them to reason directly over temporal structure rather than inferring it from raw numerical sequences. 

- T2SP is deterministic, invertible, training-free, and compatible with off-the-shelf LLMs, including API-only models. Building on T2SP, we perform time-series editing, captioning, and question answering through a unified interface – without tool calls, agentic loops, or fine-tuning. 

- Across time-series tasks and LLM models, T2SP improves reasoning performance, reduces inference time, and lowers LLM response failure rates, compared with raw-string representations, while scaling gracefully with sequence length. 

## **2 Related Works** 

### **2.1 Time-series Representations for LLMs** 

**Adapting the model to time series** has been a mainstream research direction, aligning with the standard deep learning paradigm in which data is often treated as fixed. Within this direction, two threads have emerged. 

The first line of work introduces trainable parameters into the time-series-to-LLM pipeline, whether through training encoders and adapters, or even updating the LLM itself. For instance, TEST (Sun et al., 2024) introduces a learnable encoder and prompt embedding method to enable the frozen LLM to accept time-series input. ChatTime (Wang et al., 2025) introduces an expanded vocabulary set to process time series and fine-tunes the embedding layers of LLMs. Since updating these parameters risks degrading the LLM’s general reasoning capability, ChatTime requires an additional pre-training and fine-tuning procedure to stabilize performance. Time-MQA (Kong et al., 2025) and ARTIST (Messica et al., 2026) both perform supervised fine-tuning on an open-source LLM such as Llama-3 8B and Qwen3-4B for reasoning tasks. While these methods offer a dedicated methodological contribution for time-series tasks, they require parameter updates and a non-trivial training strategy. Moreover, since supervised fine-tuning (SFT) is typically feasible only on small open-source models, it remains incompatible with the strongest closed-source LLMs, limiting its scalability. 

The second line of work adapts the model by switching to an entirely different modality: time series are rendered as visual plots (Ni et al., 2025) and processed by vision-language models (VLMs). For instance, Time-VLM (Zhong et al., 2025) renders time series as plots and uses a VLM encoder to extract embeddings. However, recent works (Wang et al., 2025; Sen et al., 2025) verify that perfor- 

2 

mance degrades monotonically with image resolution, and that VLM-based approaches struggle with fine-grained numerical tasks (Ding et al., 2026). 

**Adapting the representation** takes the opposite stance: the LLM is fixed, and time series are instead paraphrased in a form that the model can understand. This makes the approach trainingfree and directly applicable to closed-source LLMs. The most direct instantiation is to provide time series as raw strings, and a number of works (Kong et al., 2025; Xie et al., 2025; Sen et al., 2025; Messica et al., 2026) adopt such string-based representations as the primary interface between time series and LLMs, owing to their simplicity and intuitiveness. For instance, LLMTIME (Gruver et al., 2023) feeds time series into LLMs as raw strings with specialized preprocessing steps ( _e.g.,_ per-digit tokenization), and PromptCAST (Xue and Salim, 2023) rephrases the series into a structured prompt that is directly used by the LLM. However, string-based representations also have inherent limitations: tokenization cost scales with both sequence length and numerical precision, which degrades performance on long sequences (Sen et al., 2025). Nevertheless, the broad applicability of string representation across LLMs and the ease of use make it the most natural baseline for evaluating any time-series interface. Since T2SP operates on the same string-level and requires no additional training, we adopt string-representation as our primary comparison and demonstrate the benefits of T2SP across a diverse set of LLMs. 

### **2.2 Time-series Reasoning** 

Time-series reasoning is the task of utilizing the reasoning capabilities of LLMs with their contextual understanding to “reason” about time series through language. Recently, a number of timeseries reasoning tasks (Kong et al., 2025; Wang et al., 2025; Sen et al., 2025; Qiu et al., 2026) have been proposed, and at the core of these tasks lies the ability to grasp the underlying structure of a series rather than its raw values. To this end, we focus on three representative tasks that most directly demand such structural understanding: timeseries editing, captioning, and question answering. Specifically, time-series editing (Jing et al., 2024; Qiu et al., 2026) focuses on editing a source time series into a target series that encompasses userspecified attributes. This task is primarily used to examine counterfactual, or _what-if_ scenarios. Time series captioning, also referred to as open 

generation (Sen et al., 2025), is the task of describing the time series with text. Enabling a precise description of the time series plays an important role in multi-modal learning. Lastly, question answering (Wang et al., 2025) requires the model to answer natural-language questions about a given time series, verifying its ability to comprehend and reason over temporal data. In this work, we evaluate T2SP on all three tasks, demonstrating that explicit structural representation consistently benefits time-series reasoning across diverse LLMs. 

## **3 Time-series-to-Structured-Program** 

T2SP is a representation method that decomposes a time series into structural and interpretable components – trend, periodicity, and events – and expresses them in a symbolic abstract representation, enabling LLMs to reason over decomposed temporal structure rather than raw time-series values. We first formalize the notation and problem setup, then describe how each component is extracted from a raw time series through a deterministic decomposition pipeline. Building on this formulation, we show that the original time series can be faithfully reconstructed from the resulting symbolic representation, demonstrating that the decomposition preserves the essential temporal information. Finally, we present the structured program syntax used as the interface between time series and LLMs. 

**Notations.** Let _T ∈_ R<sup>+</sup> be the time horizon where we assume each time series originates from some true underlying continuous trajectory _x_ : [0 _, T_ ] _→_ R, which is observed at _N_ discrete time points _{t_ 1 _, . . . , tN } ⊂_ [0 _, T_ ]. This produces a discrete observation vector **x** = [ _x_ ( _t_ 1) _, ..., x_ ( _tN_ )]<sup>_⊤_</sup> _∈_ R<sup>_N_</sup> . An LLM, _fθ_ , performs a time-series reasoning task by taking a natural language instruction _q ∈Q_ together with a time series **x** as input, and producing an output 


![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0003-08.png)


Here, _Y_ denotes the space of natural-language outputs. Depending on the instruction specified by _q_ , the model output _y ∈Y_ may correspond to either: (i) a textual response, such as time-series _captioning_ and _question answering_ or (ii) a structural representation of a time series that can be decoded back to a reconstructed time series **x** ˆ _∈_ R<sup>_N_</sup> , as in time-series _editing_ . For simplicity, we focus on the univariate setting throughout this work. 

**Problem Formulation.** Our central question is 

3 


![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0004-00.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0004-01.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0004-02.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0004-03.png)


Figure 2: **Overview of T2SP.** A time series is decomposed into structured components – trend, periods, and events – through a sequential pipeline. Each component, together with its parameters, is expressed as a symbolic abstract representation of the time series. This program-friendly representation, along with a natural language description of each component and an instruction _q_ , is then passed to an LLM for downstream tasks. For editing, the LLM outputs an edited structural program representation, which is then reconstructed back into a time series, whereas for captioning and reasoning, it produces a natural language response. 

how to transform a raw time series **x** into a representation that enables _fθ_ to effectively reason and, therefore, produce a faithful output _y_ in Eq. (1). The current dominant approach (Xie et al., 2025; Sen et al., 2025) represents time series as a serialized string, _i.e.,_ str( **x** ), where the sequence is expressed as a list of numerical values. While this representation is straightforward and preserves the full fidelity of the original time series, it presents two major challenges for LLMs. First, the tokenization cost grows linearly with both the sequence length _N_ and the numerical precision of the value (Sen et al., 2025). Second, the model must implicitly infer high-level temporal structure ( _i.e.,_ trend, periodic patterns, and salient events) directly from raw numerical sequences, a task known to be difficult for LLMs (Zhou et al., 2025). These limitations suggest that the key bottleneck lies not only in the model, but also in the representation itself. Motivated by this observation, we propose a deterministic, training-free, and invertible transformation 


![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0004-06.png)


which maps a raw time series **x** to a structured program representation _ϕ_ ( **x** ) _∈P_ , where _P_ denotes the space of structured programs. Under this formulation, the time-series reasoning task now becomes: _y_ = _fθ_ ( _q, ϕ_ ( **x** )). In the following sections, we describe how _ϕ_ is designed to preserve the essential temporal structure of **x** while producing a representation that aligns naturally with the reasoning capabilities of LLMs. 

### **3.1 Structural Decomposition** 

We design _ϕ_ as a structural decomposition of **x** into three components: trend, periods, and events. This 

design is motivated by two key observations. First, these components together capture much of the essential structure of a time series: The trend captures the overall trajectory, period explains the recurring temporal patterns, and events characterize abrupt local deviations. Together, they provide a compact yet expressive description of a time series. Moreover, the original time series can be reconstructed by combining these components through elementwise summation, ensuring that the decomposition preserves the underlying temporal information. 

Second, structural decomposition is a wellestablished principle in both classical (Cleveland et al., 1990) and modern time-series literature (Wu et al., 2021; Kim and Lee, 2025), providing a strong foundation for extracting each component using existing methodologies. Formally, we write the decomposition of **x** as follows: 


![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0004-12.png)


where **_τ_** _,_ **_π_** _k,_ **_ϵ_** _j,_ **_r_** _∈_ R<sup>_N_</sup> are trend, period, event, and the residual, respectively and _Kp_ and _Ke_ are the number of periodic and event components. We now describe how each component is obtained through a deterministic and sequential pipeline. **Trend.** The trend represents the general direction of how the time series is moving. Here, we model **_τ_** as a composition of degree- _d_ B-spline functions 


![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0004-14.png)


where **_κ_** = [ _k_ 1 _, . . . , kM_ ] is a vector of knots and _{ci}_<sup>_M_</sup> _i_ =1<sup>arethecoefficientsfortheB-spline</sup> functions (De Boor, 1972). The discrete trend vector is then obtained by evaluating _τ_ ( _t_ ) at the observed time points, _i.e.,_ **_τ_** =[ _τ_ ( _t_ 1) _, . . . , τ_ ( _tN_ )]<sup>_⊤_</sup> . 

4 

B-splines are smooth and locally adaptive, making them suitable for trend modeling, and their knot-coefficient parameters make them interpretable. The knots and coefficients for _τ_ ( _t_ ) are obtained by solving a smoothness-penalized least-squares problem. When domain knowledge is available, the knots can be fixed ( _e.g.,_ uniform grid), with only the coefficients fitted to the data. **Periods.** The periodic components capture recurring patterns in the time series, such as seasonal patterns. Using the detrended signal **x** _−_ **_τ_** , we model each periodic component _πk_ as a sinusoid: 


![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0005-01.png)


parametrized by frequency _ωk_ and basis coefficients _ak_ and _bk_ . We select the dominant peaks (up to _Kp_ components) from the Fourier spectrum and use them as _ωk_ , where least squares is used to fit the basis coefficients. While the above formulation assumes global periodic components, time series can also have varying periodic structures between time points. As such, we also allow sinusoids to be fitted piecewise within each segment defined by the trend knot positions. These structural components are explicitly encoded in our T2SP representation. **Events.** Events represent abrupt deviations from the smooth trend and periods. Working on the residual value after subtracting the trend and periodic components, we model two different types of events: spikes and Gaussian. 


![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0005-03.png)


where _µj, aj, σj_ denote the event time, amplitude, and width, respectively, and _δ_ ( _·_ ) is the Dirac-delta function. Spikes are used for instantaneous and extreme changes ( _e.g.,_ a shock), while Gaussian events are for smooth but notable changes that are not reflected in both trend and periods. 

**Residuals or Noise.** After removing the trend, periods, and events from the original signal, what remains is a small, noise-like residual. Depending on the task, we either retain the full residual values outside of the program for exact reconstruction of the original series ( _e.g.,_ editing tasks that require returning a full time series), or parametrize it as a Gaussian, which is included as part of the program representation ( _e.g.,_ captioning or question answering, where exact reconstruction is unnecessary). 

### **3.2 Symbolic Abstract Representation** 

Building on the structural decomposition, we now aggregate the components and parameters into our symbolic abstract representation of time series (shown in Figure 2, full detail in Appendix A), and pass it to an LLM for downstream tasks. Unlike string representation that lists value-by-value, our T2SP representation makes each of the structural components _explicit_ , paired with a naturallanguage description for each component, and task instruction _q_ . This design reduces the burden on the LLM to infer structure from numbers alone, where the LLM can now reason directly over the components. Moreover, as shown in Eq. (3), we can reconstruct the original time series by adding each component, making our representation invertible. To summarize, given a raw time series, T2SP deterministically decomposes it into its structural components, converts them into a symbolic abstract representation, and passes it to an LLM along with a task-specific instruction. The resulting representation is training-free, invertible, and compatible with any off-the-shelf LLMs. 

## **4 Experiments** 

We verify the applicability of T2SP on time-series editing, captioning, and reasoning tasks. As T2SP works on any off-the-shelf LLMs, we evaluate on three closed-source models accessed via API, ranging from flagship (GPT-5.4) to lightweight (Claude-haiku-4.5, Gemini-3.1 -flash-lite), and an open-source model (Qwen-3.5-9B). Within each LLM, we compare three different representations of time series: string ( **raw** ), visual rendering ( **vision** ), and T2SP ( **ours** ). In addition, we compare against task-specialized baselines, introduced in each task’s subsection. We provide the details of all datasets in Appendix B. 

### **4.1 Time-series Editing** 

A key advantage of representing time series as structural components is that it enables _targeted editing_ . When time series are represented as raw sequences or images, the LLM must implicitly reason over individual values or pixels, making localized modifications difficult. In contrast, T2SP exposes the time series as a symbolic abstract representation that LLMs can manipulate directly (Gao et al., 2023). This allows the model to modify only the intended component while preserving the remaining structure, providing precise edits in a 

5 

|Method||**Trend**<br>|||**Periodic**<br>|||**Event**<br>|||**Average**<br>||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Fid. _↑_|Pre._↑_|Succ._↑_|Fid._↑_|Pre._↑_|Succ._↑_|Fid._↑_|Pre._↑_|Succ._↑_|Fid._↑_|Pre._↑_|Succ._↑_|
|GPT-5.4|||||||||||||
|Raw|0.829|0.589|0.925|0.653|0.562|0.938|0.776|0.911|0.975|0.753|0.687|0.946|
|Vision|0.452|0.389|0.875|0.489|0.391|0.800|0.538|0.270|0.875|0.493|0.350|0.850|
|T2SP(Ours)|**0.976**|**0.878**|**1.000**|**0.866**|**0.791**|**1.000**|**0.880**|**0.984**|**1.000**|**0.907**|**0.884**|**1.000**|
|Claude-haiku-4.5<br>|||||||||||||
|Raw|0.377|0.668|0.963|0.495|0.653|**1.000**|0.718|0.904|0.988|0.530|0.742|0.983|
|Vision|0.438|0.198|**0.988**|0.536|0.175|**1.000**|0.462|0.000|0.988|0.479|0.124|0.992|
|T2SP(Ours)|**0.844**|**0.862**|**0.988**|**0.866**|**0.791**|**1.000**|**0.880**|**0.984**|**1.000**|**0.863**|**0.879**|**0.996**|
|Gemini-3.1-flash<br>|-lite<br>||||||||||||
|Raw|0.509|0.582|0.912|0.509|0.615|0.988|0.732|0.926|**1.000**|0.583|0.708|0.967|
|Vision|0.312|0.391|0.762|0.482|0.259|0.750|0.470|0.272|0.738|0.421|0.307|0.750|
|T2SP(Ours)|**0.971**|**0.877**|**1.000**|**0.868**|**0.791**|**1.000**|**0.867**|**0.967**|0.975|**0.902**|**0.879**|**0.992**|
|Qwen-3.5-9B|||||||||||||
|Raw|0.564|0.424|0.725|0.469|0.513|0.838|0.595|0.760|0.812|0.543|0.566|0.792|
|Vision|0.478|0.204|0.762|0.727|0.406|0.950|0.639|0.073|**1.000**|0.615|0.228|0.904|
|T2SP(Ours)|**0.935**|**0.847**|**0.963**|**0.866**|**0.791**|**1.000**|**0.874**|**0.993**|**1.000**|**0.892**|**0.877**|**0.988**|
|_Others_|||||||||||||
|ChatTime-7B|0.358|0.111|0.800|0.307|0.091|0.800|0.402|0.000|0.800|0.356|0.067|0.800|
|Verbal-TS<sup>_∗_</sup>|0.351|0.419|1.000|0.501|0.118|1.000|0.495|0.000|1.000|0.452|0.179|1.000|
|InstructTime<sup>_∗_</sup>|0.598|0.616|1.000|0.638|0.311|1.000|0.503|0.044|1.000|0.580|0.324|1.000|



Table 1: **Performance on the TSEdit benchmark.** Fid., Pre., and Succ. denote edit fidelity, preservation, and success rate, respectively. We compared our T2SP with raw time series (Raw) and image (Vision) representation using the same LLM as a backbone. We also compared with training-based models (denoted with *), where 6000 samples were used for model training. For failed samples, where the model produced an invalid output format, Fid. and Pre. were assigned a score of zero. 

token-efficient manner. Moreover, since edits are performed directly on symbolic components, the modifications made by the LLM ( _e.g.,_ modification, insertion, deletion) remain human-interpretable. 

**Setup.** We evaluate the editing capability of T2SP on two different tasks. First, we construct and evaluate on **TSEdit** , a synthetic benchmark consisting of time series paired with natural-language editing instructions targeting trend, periodic, or event components ( _e.g., Remove the anomaly at t_ = 50), along with a corresponding ground-truth edited time series. Since the synthetic data are generated by independently sampling and composing trend, periodic, and event components, the groundtruth edits come directly from the data generation process and are independent of our decomposition method. Second, we evaluate on ETTh1 (Wu et al., 2021), a real-world oil temperature forecasting dataset, with editing instructions that mimic the unstructured, ambiguous phrasing of real users. For instance, instruction such as _“Remove the sudden drop around the center”_ leaves the notion of _center_ open to interpretation. For this task, we use human evaluation because component-level ground truth is not well defined for real-world time series. The key metrics for both tasks are: _fidelity_ ( _i.e.,_ performing the targeted edit) and _preservation_ ( _i.e.,_ leaving the other components intact). In addition, we report the _success rate_ , measuring how often the LLM produces a response that conforms to the 


![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0006-04.png)


Figure 3: **Time Taken and Success Rate Across Sequence Length.** The left and right axes represent the time taken (seconds) to perform the editing and the success rate, respectively. The three representations perform comparably up to a sequence length of 256, beyond which the raw and visionbased baselines deteriorate rapidly, while T2SP remains stable. 

required output format. In addition to the LLMbased methods, we compare with a time-series language model, ChatTime-7B (Wang et al., 2025); a text-conditioned time-series generative model, Verbal-TS (Gu et al., 2025); and the state-of-the-art editing model, InstructTime (Qiu et al., 2026). **TSEdit Results.** Table 1 shows that T2SP consistently achieves the strongest performance across all component types ( _i.e.,_ trend, periodic, and event edits) and across all LLM backbones. Overall, editing performance improves with model capability for every representation, with GPT-5.4 performing best, followed by smaller models such as Gemini, Claude, and Qwen. This trend highlights the importance of being able to leverage highly 

6 

|Human Evaluation|Fid. _↑_|Pre. _↑_|Overall_↑_|
|---|---|---|---|
|GPT-5.4||||
|T2SPvs. Raw|58.9%|56.7%|60.0%|
|T2SPvs. Vision|84.3%|91.4%|92.9%|
|Claude-haiku-4.5||||
|T2SPvs. Raw|84.4%|63.3%|80.0%|
|T2SPvs. Vision|91.4%|97.1%|92.9%|
|Qwen3.5-9b||||
|T2SPvs. Raw|79.2%|73.6%|79.2%|
|T2SPvs. Vision|88.6%|100.0%|88.6%|



Table 2: **Pairwise Evaluation on ETTh1.** Each row compares T2SP against a baseline; values denote the Win Rate (%) of T2SP over the baseline. Fid. and Pre. denotes the fidelity and preservation. Overall is the final preference. Detailed Win/Tie/Lose rates are provided in Appendix C. 

capable closed-source LLMs without additional task-specific training. A notable observation is that T2SP achieves a substantially better balance between fidelity and preservation than competing representations, which often improve one metric at the expense of the other. We attribute this behavior to the explicit structural decomposition provided by our symbolic abstraction: because each component is independently represented, the LLM can precisely modify the targeted component while leaving the remaining structure untouched. Importantly, T2SP achieves these gains in a fully training-free manner, whereas models such as Verbal-TS and InstructTime are extensively trained on synthetic editing samples constructed from combinations of the same underlying editing operations. 

**Human Evaluation.** We further conduct a pairwise human evaluation on the real-world ETTh1 dataset. We recruit ten annotators, each of whom is presented with an original time series, an editing instruction, and two edited outputs presented in randomized order without method labels. One time series is produced by T2SP and the other by either the raw or vision-based baseline. Annotators are then asked to select the edited time series that better satisfies the editing instruction. We report the win rate of T2SP in Table 2; full details and qualitative examples are provided in Appendix C. Win rates above 50% indicate that annotators consistently preferred outputs generated by T2SP over the competing representations. The performance gap is particularly large against the vision-based baseline, suggesting that image-based representations are poorly suited for editing tasks that require localized and structurally coherent modifications. 

**Time Taken and Success Rate.** We analyze the time taken to perform the editing task and the suc- 

|N-shot|Method|**Wa**<br>|**fer**<br>|**ECG**<br>|**200**<br>|
|---|---|---|---|---|---|
|||Acc. _↑_|F1_↑_|Acc. _↑_|F1_↑_|
||Raw<br>|0.465<br>|0.360<br>|0.560<br>|0.476<br>|
|_zero-shot_|Vision<br>|0.495<br>|0.363<br>|0.570<br>|0.402<br>|
||T2SP(Ours)|**0.505**|**0.368**|**0.660**|**0.587**|
||Raw<br>|0.563<br>|0.544<br>|0.640<br>|0.506<br>|
|_1-shot_|Vision<br>|0.415<br>|0.405<br>|0.630<br>|0.432<br>|
||T2SP(Ours)|**0.620**|**0.611**|**0.670**|**0.526**|
||Raw<br>|0.630<br>|0.617<br>|0.620<br>|0.382<br>|
|_3-shot_|Vision<br>|0.495<br>|0.412<br>|0.670<br>|0.474<br>|
||T2SP(Ours)|**0.835**|**0.835**|**0.690**|**0.634**|
||Raw<br>|0.690<br>|0.689<br>|0.630<br>|0.469<br>|
|_5-shot_|Vision<br>|0.520<br>|0.417<br>|0.590<br>|0.516<br>|
||T2SP(Ours)|**0.850**|**0.849**|**0.710**|**0.596**|
||Raw|0.650|0.633|0.650|0.442|
|_20-shot_|Vision<br>|0.560<br>|0.546<br>|0.650<br>|0.442<br>|
||T2SP(Ours)|**0.895**|**0.894**|**0.730**|**0.668**|



Table 3: **Caption-based Classification.** For each representation, captions are first generated from the time series, and classification is performed using only the generated captions. Acc. and F1 denote accuracy and macro-F1, respectively. 

cess rate based on the sequence length in Figure 3. We observe that raw and vision-based approaches scale poorly in both runtime and success rate as sequence length increases. We conjecture that these representations incur input and output costs that scale linearly with sequence length, increasing both the reasoning cost and the likelihood of malformed outputs. In contrast, T2SP remains robust, as even long time series can be faithfully expressed with our symbolic abstract representation. 

### **4.2 Time-series Captioning** 

Time-series captioning is the task of producing a natural language description of a time series, where this caption can be used for multi-modal learning, and downstream reasoning (Langer et al., 2025). A meaningful caption, in this role, must preserve the structural content of the time series with sufficient fidelity, such that the underlying patterns remain recoverable from the description alone. 

**Setup.** To assess the utility of T2SP for captioning, we adopt a _reference-free_ evaluation based on downstream classification performance. Such evaluation can avoid the stylistic biases inherent in human-written reference captions (Hessel et al., 2021). Specifically, we generate a natural-language caption for each time series and use a separate LLM to classify the sample using only its caption. For this task, we utilize the Wafer and ECG200 datasets (Dau et al., 2019), where classes are distinguished by fine-grained temporal structures rather than by the holistic shape of the time series. We also evaluate a few-shot setup, where we provide 1 _,_ 3 _,_ 5 _,_ and 20 samples for each class as a reference. 

7 

|Method|**TSQ**<br>|**A**<br>|**TR**<br>|**QA**<br>|**ET**<br>|**I**<br>|
|---|---|---|---|---|---|---|
||ACC_↑_|F1_↑_|ACC_↑_|F1_↑_|ACC_↑_|F1_↑_|
|Random Guess|0.333|0.333|0.369|0.322|0.250|0.250|
|GPT-5.4|||||||
|Raw<br>|0.818<br>|0.645<br>|0.740<br>|0.851<br>|0.680<br>|0.809<br>|
|Vision|0.810|0.646|0.710|0.830|**0.880**|**0.936**|
|T2SP(Ours)|**0.857**|**0.686**|**0.815**|**0.898**|0.840|0.909|
|Claude-haiku-4<br>|.5<br>||||||
|Raw|0.758|0.599|0.700|0.824|0.565|0.720|
|Vision|0.732|0.580|0.750|0.857|0.685|0.813|
|T2SP(Ours)|**0.852**|**0.681**|**0.760**|**0.864**|**0.910**|**0.955**|
|Gemini-3.1-fla<br>|sh-lite<br>||||||
|Raw<br>|0.768<br>|0.610<br>|0.730<br>|0.844<br>|0.705<br>|0.818<br>|
|Vision|0.766|0.608|0.725|0.719|0.925|0.961|
|T2SP(Ours)|**0.859**|**0.683**|**0.760**|**0.864**|**0.930**|**0.962**|
|Qwen-3.5-9B<br>|||||||
|Raw|0.745|0.579|0.735|0.847|0.815|0.901|
|Vision|0.743|0.591|**0.755**|**0.860**|0.885|0.939|
|T2SP(Ours)|**0.867**|**0.694**|0.727|0.842|**0.950**|**0.974**|
|ChatTime-7B|0.521|0.516|0.314|0.245|0.220|0.100|



Table 4: Performance comparison across TSQA, TRQA, and ETI tasks. Best scores in **bold** . 

**Caption Results.** Table 3 reports the classification results using the Gemini-3.1-flash-lite as both the caption generator and classifier for all representations. We report additional model results and qualitative examples in Appendix D. T2SP achieves the best accuracy and F1-score across both datasets and few-shot setups. Notably, on Wafer, the gain from additional samples is particularly pronounced for T2SP– F1 rises from 0.368 to 0.835 with just three shots, whereas the corresponding gains for vision representation remain modest (vision: 0.363 to 0.412). We attribute this to the nature of a visionbased approach: while the model is suitable in capturing the holistic shape of a time series, they often miss fine-grained temporal structures such as periodicity or localized events. In contrast, T2SP exposes trend, periodicity, and events as explicit input components, allowing the generated captions to cover both the holistic shape and the detailed temporal structure of the time series. 

### **4.3 Time-series Reasoning** 

Time-series reasoning is the task of answering a question about a given time series, typically formulated as a multiple-choice question where the LLM selects the correct answer from a set of candidates (Kong et al., 2025; Wang et al., 2025). Compared to captioning, reasoning provides a stricter test of structural understanding, as each answer is judged against a ground truth. This makes reasoning a suitable testbed for T2SP, where we can evaluate whether the LLM can effectively reason over our symbolic abstract representations. 

**Setup.** We evaluate on three time-series reason- 

ing benchmarks that span complementary question types: TSQA (Wang et al., 2025) asks whether a time series satisfies a specified structural pattern, while ETI (Merrill et al., 2024) and TRQA (Jing et al.) require selecting the explanation that best matches a given time series. We compare T2SP against raw and vision-based representations and to ChatTime-7B (Wang et al., 2025). 

**Results.** In Table 4, T2SP is the best performing representation in 10 out of 12 cases. The performance gain is especially notable in both the TSQA and ETI tasks, which require reasoning over the temporal structures of the time series ( _e.g., which structure has a linearly increasing trend_ ). In particular, for the Claude model on the ETI task, the raw representation achieves only 56.5% accuracy, whereas T2SP reaches 91.0%, demonstrating a substantial performance gap of over 34 percentage points. We also note that vision-based representation is a competitive baseline, an observation that aligns with existing works (Sen et al., 2025). In fact, the two cases where T2SP underperforms are both lost to vision. This observation suggests that existing benchmarks may, to some extent, be solvable through purely visual cues, pointing to the need for the development of benchmarks that require more explicit reasoning over the structural properties of time series rather than those that can be solved by visual inspection. 

## **5 Conclusion** 

In this work, we propose T2SP, a novel time-series representation method for LLM interfacing. Specifically, T2SP decomposes a time series into structural components – trend, periods, and salient events – and aggregates them into a structured symbolic representation that is re-expressed in a program-friendly form. Then, the LLM reasons over this structured representation space instead of the raw numerical series. As such, T2SP aligns the input with the symbolic and code-like modalities LLMs were natively pretrained on, allowing them to apply their existing reasoning capabilities directly. Notably, our T2SP representation is deterministic, training-free, and compatible with any off-the-shelf LLM, including the strongest performing closed-source models accessible only via APIs. We demonstrate T2SP’s capability on time-series editing, caption generation, and reasoning, establishing it as an effective interface that connects time series and the reasoning capabilities of LLMs. 

8 

## **Limitations** 

In this work, we proposed T2SP to represent a time series as a symbolic abstract representation – composed of trend, periods, and events – that works as an effective interface between time series and LLMs. While our decomposition faithfully captures the structural composition of a time series, the trend–period–event decomposition may not be the most suitable abstraction for every time-series task. For instance, electrocardiogram (ECG) signals are characterized by domain-specific morphological primitives such as the P, Q, R, S, and T waves, whose clinical meaning is tied to their precise shape and relative timing rather than to a global trend or periodicity. Such fine-grained, domainspecific structures are not directly captured by our trend–period–event decomposition, and a representation tailored to these primitives would likely be more effective. Therefore, we acknowledge that our decomposition strategy may not be universally optimal across all tasks and datasets. Our goal in this paper is not to argue that our decomposition is the optimal strategy, but rather to demonstrate the potential of structural, program-friendly representations as an effective interface between time series and LLMs. We view the design of domain-specific decompositions as a promising direction for future work. 

## **Ethical considerations** 

This work introduces a representation method for time-series analysis with large language models. The contribution is methodological. Also, our experiments are conducted on both a synthetic dataset (explained in Section B.1) and publicly available time-series benchmarks. We do not collect new data from human subjects beyond the human evaluation described in Section C, for which annotators were recruited with informed consent and the evaluation involved no sensitive or personally identifying information. We do not foresee direct ethical concerns or potential for misuse beyond those generally associated with applying large language models to numerical and temporal data. 

## **References** 

- Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, and 1 others. 2023. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ . 

- Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde De Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, and 1 others. 2021. Evaluating large language models trained on code. _arXiv preprint arXiv:2107.03374_ . 

- Wenhu Chen, Xueguang Ma, Xinyi Wang, and William W Cohen. 2023. Program of thoughts prompting: Disentangling computation from reasoning for numerical reasoning tasks. _Transactions on Machine Learning Research_ . 

- Robert B Cleveland, William S Cleveland, Jean E McRae, Irma Terpenning, and 1 others. 1990. Stl: A seasonal-trend decomposition. _J. off. Stat_ , 6(1):3–73. 

- Hoang Anh Dau, Anthony Bagnall, Kaveh Kamgar, Chin-Chia Michael Yeh, Yan Zhu, Shaghayegh Gharghabi, Chotirat Ann Ratanamahatana, and Eamonn Keogh. 2019. The ucr time series archive. _IEEE/CAA Journal of Automatica Sinica_ , 6(6):1293– 1305. 

- Carl De Boor. 1972. On calculating with b-splines. _Journal of Approximation theory_ , 6(1):50–62. 

- Yueyang Ding, HaoPeng Zhang, Rui Dai, Yi Wang, Tianyu Zong, Kaikui Liu, and Xiangxiang Chu. 2026. Llatisa: Towards difficulty-stratified time series reasoning from visual perception to semantics. _arXiv preprint arXiv:2604.17295_ . 

- Elizabeth Fons, Rachneet Kaur, Soham Palande, Zhen Zeng, Tucker Balch, Manuela Veloso, and Svitlana Vyetrenko. 2024. Evaluating large language models on time series feature understanding: A comprehensive taxonomy and benchmark. In _Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing_ , pages 21598–21634. 

- Luyu Gao, Aman Madaan, Shuyan Zhou, Uri Alon, Pengfei Liu, Yiming Yang, Jamie Callan, and Graham Neubig. 2023. Pal: Program-aided language models. In _International conference on machine learning_ , pages 10764–10799. PMLR. 

- Nate Gruver, Marc Finzi, Shikai Qiu, and Andrew G Wilson. 2023. Large language models are zero-shot time series forecasters. _Advances in neural information processing systems_ , 36:19622–19635. 

- Shuqi Gu, Chuyue Li, Baoyu Jing, and Kan Ren. 2025. Verbalts: Generating time series from texts. In _Fortysecond International Conference on Machine Learning_ . 

- Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, and Jacob Steinhardt. 2021. Measuring mathematical problem solving with the math dataset. In _Thirtyfifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 2)_ . 

9 

- Jack Hessel, Ari Holtzman, Maxwell Forbes, Ronan Le Bras, and Yejin Choi. 2021. Clipscore: A reference-free evaluation metric for image captioning. In _Proceedings of the 2021 conference on empirical methods in natural language processing_ , pages 7514– 7528. 

- Ming Jin, Yifan Zhang, Wei Chen, Kexin Zhang, Yuxuan Liang, Bin Yang, Jindong Wang, Shirui Pan, and Qingsong Wen. 2024. Position: What can large language models tell us about time series analysis. In _Forty-first international conference on machine learning_ . 

- Baoyu Jing, Sanhorn Chen, Lecheng Zheng, Boyu Liu, Zihao Li, Jiaru Zou, Tianxin Wei, Zhining Liu, Zhichen Zeng, Ruizhong Qiu, and 1 others. Trqa: Time series reasoning question and answering benchmark. 

- Baoyu Jing, Shuqi Gu, Tianyu Chen, Zhiyu Yang, Dongsheng Li, Jingrui He, and Kan Ren. 2024. Towards editing time series. _Advances in Neural Information Processing Systems_ , 37:37561–37593. 

- Jaeho Kim and Seulki Lee. 2025. Transpl: Vq-code transition matrices for pseudo-labeling of time series unsupervised domain adaptation. In _International Conference on Machine Learning_ , pages 30462–30479. PMLR. 

- Yaxuan Kong, Yiyuan Yang, Yoontae Hwang, Wenjie Du, Stefan Zohren, Zhangyang Wang, Ming Jin, and Qingsong Wen. 2025. Time-mqa: Time series multitask question answering with context enhancement. In _Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pages 29736–29753. 

- Patrick Langer, Thomas Kaar, Max Rosenblattl, Maxwell A Xu, Winnie Chow, Martin Maritsch, Robert Jakob, Ning Wang, Juncheng Liu, Aradhana Verma, and 1 others. 2025. Opentslm: Time-series language models for reasoning over multivariate medical text-and time-series data. _arXiv preprint arXiv:2510.02410_ . 

- Chris Lu, Cong Lu, Robert Tjarko Lange, Jakob Foerster, Jeff Clune, and David Ha. 2024. The ai scientist: Towards fully automated open-ended scientific discovery. _arXiv preprint arXiv:2408.06292_ . 

- Mike A Merrill, Mingtian Tan, Vinayak Gupta, Thomas Hartvigsen, and Tim Althoff. 2024. Language models still struggle to zero-shot reason about time series. In _Findings of the Association for Computational Linguistics: EMNLP 2024_ , pages 3512–3533. 

- Shvat Messica, Jiawen Zhang, Kevin Li, Theodoros Tsiligkaridis, and Marinka Zitnik. 2026. Adaptive time series reasoning via segment selection. _arXiv preprint arXiv:2602.18645_ . 

- Jingchao Ni, Ziming Zhao, ChengAo Shen, Hanghang Tong, Dongjin Song, Wei Cheng, Dongsheng Luo, and Haifeng Chen. 2025. Harnessing vision models 

for time series analysis: A survey. _arXiv preprint arXiv:2502.08869_ . 

- Long Phan, Alice Gatti, Ziwen Han, Nathaniel Li, Josephina Hu, Hugh Zhang, Chen Bo Calvin Zhang, Mohamed Shaaban, John Ling, Sean Shi, and 1 others. 2025. Humanity’s last exam. _arXiv preprint arXiv:2501.14249_ . 

- Jiaxing Qiu, Dongliang Guo, Brynne Sullivan, Teague R Henry, and Thomas Hartvigsen. 2026. Instructionbased time series editing. In _Proceedings of the 32nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining V. 1_ , pages 1216–1227. 

- Medhasweta Sen, Zachary Gottesman, Jiaxing Qiu, C Bayan Bruss, Nam Nguyen, and Tom Hartvigsen. 2025. Bedtime: A unified benchmark for automatically describing time series. _arXiv preprint arXiv:2509.05215_ . 

- Chenxi Sun, Hongyan Li, Yaliang Li, and Shenda Hong. 2024. Test: Text prototype aligned embedding to activate llm’s ability for time series. In _International Conference on Learning Representations_ , volume 2024, pages 37854–37881. 

- Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, and 1 others. 2023. Llama: Open and efficient foundation language models. _arXiv preprint arXiv:2302.13971_ . 

- Chengsen Wang, Qi Qi, Jingyu Wang, Haifeng Sun, Zirui Zhuang, Jinming Wu, Lei Zhang, and Jianxin Liao. 2025. Chattime: A unified multimodal time series foundation model bridging numerical and textual data. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 39, pages 12694–12702. 

- Haixu Wu, Jiehui Xu, Jianmin Wang, and Mingsheng Long. 2021. Autoformer: Decomposition transformers with auto-correlation for long-term series forecasting. _Advances in neural information processing systems_ , 34:22419–22430. 

- Zhe Xie, Zeyan Li, Xiao He, Longlong Xu, Xidao Wen, Tieying Zhang, Jianjun Chen, Rui Shi, and Dan Pei. 2025. Chatts: Aligning time series with llms via synthetic data for enhanced understanding and reasoning. _Proceedings of the VLDB Endowment_ , 18(8):2385– 2398. 

- Hao Xue and Flora D Salim. 2023. Promptcast: A new prompt-based learning paradigm for time series forecasting. _IEEE Transactions on Knowledge and Data Engineering_ , 36(11):6851–6864. 

- Siru Zhong, Weilin Ruan, Ming Jin, Huan Li, Qingsong Wen, and Yuxuan Liang. 2025. Time-vlm: Exploring multimodal vision-language models for augmented time series forecasting. In _International Conference on Machine Learning_ , pages 78478–78497. PMLR. 

10 

Tianyi Zhou, Deqing Fu, Mahdi Soltanolkotabi, Robin Jia, and Vatsal Sharan. 2025. Fone: Precise singletoken number embeddings via fourier features. _arXiv preprint arXiv:2502.09741_ . 

11 

## **A Full T2SP Representation** 

We provide a visual illustration of the full T2SP representation for a given time series. Following the deterministic decomposition pipeline described in Section 3, a raw series is decomposed into its structural components – trend, periods, and events – with the residual either retained for exact reconstruction or parametrized as a Gaussian, depending on the downstream task. 


![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0012-02.png)


Figure 4: **Example of T2SP representation.** We format the trend, events, and periods into a structured symbolic abstract representation. This representation is human-interpretable and invertible. 


![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0012-04.png)


Figure 5: **Decomposition from T2SP.** We provide a visual illustration of the decomposition. 

## **B Datasets & Baseline Implementation** 

### **B.1 TSEdit Dataset** 

We construct the **TSEdit** dataset to evaluate instruction-based time-series editing. Prior work on time-series editing (Qiu et al., 2026) adopts an _attribute-based_ formulation, where edits are framed as adding or removing the presence of a predefined attribute in the series ( _e.g.,_ the existence of bradycardia, a type of abnormal heart event). While this formulation is useful for controlled evaluation, it differs from how humans typically describe edits in practice, where instructions often specify _which_ component to change and _how_ – for example, “remove the anomaly at _t_ = 50” or “flatten the trend”. To better reflect this setting, we construct TSEdit by synthetically generating pairs of free-form natural-language instructions and their corresponding ground-truth target series. 

To generate each time series, we first initialize generating functions for the trend, period, and event components, and aggregate them to form the final series. This construction enables us to access the underlying attributes of each component ( _e.g.,_ trend slope, periodicity, event time), and consequently to the ground-truth attributes of the edited series. Importantly, **we emphasize that each series is** **_constructed from_ its components, rather than the components being inferred from a pre-existing series.** As a result, even our own decomposition does not recover the original generating parameters exactly: the generating functions and our decomposition primitives do not share the same parametrization, so applying our representation to TSEdit is not a trivial identity mapping. This ensures that TSEdit does not artificially favor our representation, and that our evaluation reflects the genuine difficulty of recovering and editing the underlying structure. Below, we explain the type of instruction used for each task. We will publicly release the dataset upon acceptance. 

### **B.2 Baseline Implementation for TSEdit** 

Instruction-based time-series editing has only been recently studied, and to the best of our knowledge, InstructTime (Qiu et al., 2026) is the only existing method that directly targets this task. We therefore use InstructTime as the primary editing baseline and follow its original training and inference procedure. In addition, to cover a broader editing paradigm, we consider a time-series generationbased setting from TEdit (Jing et al., 2024), where 

12 

Table 5: Overview of datasets used in this paper 

|Dataset|Task|# Train|# Test|Sequence Length|Note|
|---|---|---|---|---|---|
|_Editing_||||||
|TSEdit-Trend|Editing||80|_{_32_,_64_,_256_,_1024_,_4096_}_|16 test samples per length|
|TSEdit-Period|Editing|6,000|80|_{_32_,_64_,_256_,_1024_,_4096_}_|We used training samples only to train the baseline models|
|TSEdit-Event|Editing||80|_{_32_,_64_,_256_,_1024_,_4096_}_|(InstructTime, Verbal-TS), which require training for time-series editing.|
|ETTh1|Editing|–|15|1440|Human evaluation; 5 curated samples each for Trend, Period, Event|
|_Captioning_||||||
|Wafer|Classifcation|6,164|200|–|Ti l d  fht l|
|ECG200|Classifcation|100|100|96|ran sampes use as ew-so exampes.|
|_Question Answering_||||||
|TSQA-Trend|MCQ|–|100|_{_64_,_128_,_256_,_512_}_|Stratifed sampling by length (100 samples)|
|TSQA-Seasonality|MCQ|–|100|_{_64_,_128_,_256_,_512_}_|Stratifed sampling by length (100 samples)|
|TSQA-Volatility|MCQ|–|100|_{_64_,_128_,_256_,_512_}_|Stratifed sampling by length (100 samples)|
|TSQA-Outliers|MCQ|–|100|_{_64_,_128_,_256_,_512_}_|Stratifed sampling by length (100 samples)|
|TRQA|MCQ, T/F|–|200|131_±_64|Randomly sampled (200 samples)|
|ETI|MCQ|–|200|422_±_376|Randomly sampled (200 samples)|



time-series editing is performed by generating a new time series that reflects the desired changes rather than directly modifying the input series. In this setting, the editing instruction specifies the properties of the target output series, and the model generates a series that satisfies those properties from scratch. Based on this perspective, we include Verbal-TS (Gu et al., 2025) as an editingfrom-scratch baseline. Since both InstructTime and Verbal-TS require training samples for editing, we independently generate 6000 training samples from the same distribution of TSEdit. We also generate caption pairs that reflect the attributes needed to train InstructTime and Verbal-TS. At inference time, both models generate the edited time series conditioned on the caption of the target series that reflects the requested edit. 

## **C Time Series Editing: Human Evaluation** 

Table 6: Edit operations defined in the TSEdit dataset. Each operation modifies a specific structural component (trend, periodicity, or event) of the input series. _N_ denotes a randomly sampled magnitude parameter. 

|Operation|Description|
|---|---|
|_Trend_||
|edit_flatten<br>edit_increase_slope<br>edit_decrease_slope<br>edit_reverse|Flatten the trend to be constant<br>Increase the slope by+_N_%<br>Decrease the slope by_−N_%<br>Reverse the trend direction|
|_Periodic_||
|periodic_remove_largest<br>periodic_amp_increase<br>periodic_amp_decrease<br>periodic_change_period|Zero out the seasonality<br>Increase amplitude by+_N_%<br>Decrease amplitude by_N_%<br>Change the period by_±N_%|
|_Event_||
|event_remove_largest<br>event_remove_second<br>event_shift<br>event_reduce_amp|Remove the largest event<br>Remove the second largest event<br>Shift the largest event by_N_ time steps<br>Reduce amplitude largest event to_N_%|



We conduct a pairwise human evaluation to assess whether the edited time series by T2SP better reflects a given editing instruction compared to alternative representations ( _i.e.,_ raw, vision). 

**Data curation.** For this evaluation, we curated 15 samples of length 1440 (equivalent to a 2-month period) from the real-world ETTh1 dataset. We could not select data points at random, since each human instruction must be matched to a segment that actually exhibits the referenced structure – for instance, an instruction such as _“remove the anomaly at the center”_ requires the corresponding segment to contain an anomalous event at its center. Moreover, since the evaluation requires pairwise comparison across every combination of representation and LLM backbone, this sample size kept the annotation workload manageable within a single onehour session per annotator, while still being large enough to provide a balanced coverage of the three structural components (5 samples each for trend, period, and event). 

**Annotator Recruitment.** We recruited a total of 10 annotators with prior knowledge in time-series analysis. The annotators were evenly split into two groups: 5 evaluated T2SP against the raw string representation, and the remaining 5 evaluated T2SP against the vision-based representation. We paid $6 USD per annotator for their participation, which took approximately 40 minutes to complete. **Evaluation Method.** We built a streamlit-based annotation framework, where for each evaluation sample, annotators are shown three pieces of information: the original time series, a natural-language editing instruction, and two edited time series produced by two different methods. As illustrated in Figure 6, the original time series is provided together with the instruction describing how the series should be modified. The two candidate edited 

13 

|Baseline|Fid. (**Win**/Tie/Lose)|Pre. (**Win**/Tie/Lose)|Overall (**Win**/Tie/Lose)|
|---|---|---|---|
|_GPT-5.4_||||
|T2SPvs. Raw|**58.9**/ 4.4 / 36.7|**56.7**/ 11.1 / 32.2|**60.0**/ 5.6 / 34.4|
|T2SPvs. Vision|**84.3**/ 8.6 / 7.1|**91.4**/ 7.1 / 1.4|**92.9**/ 2.9 / 4.3|
|_Claude-haiku-4.5_||||
|T2SPvs. Raw|**84.4**/ 7.8 / 7.8|**63.3**/ 22.2 / 14.4|**80.0**/ 12.2 / 7.8|
|T2SPvs. Vision|**91.4**/ 5.7 / 2.9|**97.1**/ 1.4 / 1.4|**92.9**/ 5.7 / 1.4|
|_Qwen3.5-9b_||||
|T2SPvs. Raw|**79.2**/ 8.3 / 12.5|**73.6**/ 12.5 / 13.9|**79.2**/ 11.1 / 9.7|
|T2SPvs. Vision|**88.6**/ 2.9 / 8.6|**100.0**/ 0.0 / 0.0|**88.6**/ 11.4 / 0.0|



Table 7: **Full results for human evaluation on ETTh1 dataset.** Full Win/Tie/Lose ratios corresponding to the summary results in Table 2. Each row compares T2SP against a baseline; **Win** /Tie/Lose values are reported from the perspective of T2SP. Fid. and Pre. denote fidelity and preservation, respectively. 

results are then displayed side by side as Method A and Method B. To ensure a fair comparison, the evaluation is conducted in a blind and randomized manner. Specifically, one of the two edited results is generated by T2SP, while the other is generated by a baseline method, either the raw time-series or the vision-based baseline. The method identities are not revealed to the annotators. In addition, the order of the two results is randomly shuffled for each sample. 

**Evaluation.** Each sample is evaluated along three criteria: Fidelity, Preservation, and Overall Preference. Fidelity measures how accurately the edited time series follows the requested modification in the instruction. In other words, annotators are asked to judge which result better reflects the intended edit, such as increasing, decreasing, shifting, or otherwise modifying the specified region or pattern. Preservation measures whether the parts of the time series that are not mentioned in the instruction remain unchanged. This criterion is important because a desirable editing method should modify only the instructed aspects while preserving the remaining temporal structure of the original series. Finally, Overall Preference asks annotators to choose the result that is better overall, considering both instruction fidelity and preservation of irrelevant regions. The Similar option is provided when the two edited results are difficult to distinguish or when neither result is clearly better under the corresponding criterion. 

**Results.** We aggregate the annotations by computing the win rate of T2SP against each baseline. A win is counted when the annotator selects the result produced by T2SP over the competing baseline for a given criterion. Responses marked as 

Similar are treated as ties and are not counted as wins for either method. The resulting win rates are reported in Table 7. A win rate above 50% indicates that human annotators more frequently prefer T2SP over the corresponding baseline. The results show that T2SP is preferred over both baselines, with a particularly large margin against the vision-based baseline. This indicates that visionbased representations may struggle to support such fine-grained instructions, whereas T2SP more effectively performs targeted edits while preserving the remaining struct ~~ure~~ of the original signal. 


![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0014-06.png)


Figure 6: **Streamlit-based Annotation Framework.** We capture the annotation interface used in our experiment. 

14 


![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-00.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-01.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-02.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-03.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-04.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-05.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-06.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-07.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-08.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-09.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-10.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-11.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-12.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-13.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-14.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-15.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-16.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-17.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-18.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-19.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-20.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-21.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-22.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-23.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-24.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-25.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-26.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-27.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-28.png)



![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0015-29.png)


Figure 7: **Editing results on ETTh1 task.** The grey and red lines show the original and edited time series, respectively. T2SP produces precise, component-level edits across trend, periodicity, and event instructions, while Raw and Vision baselines often fail to localize changes or even corrupt unrelated structure. 

|N-shot|Method|**G**|**emini-3.**|**1-fash-lit**|**e**||**Claude-h**|**aiku-4.5**||
|---|---|---|---|---|---|---|---|---|---|
|||**Wa**<br>|**fer**<br>|**ECG**<br>|**200**<br>|**Wa**<br>|**fer**<br>|**ECG**<br>|**200**<br>|
|||Acc_↑_|F1_↑_|Acc_↑_|F1_↑_|Acc_↑_|F1_↑_|Acc_↑_|F1_↑_|
||Raw|0.465|0.360|0.560|0.476|**0.585**|**0.532**|0.540|0.452|
|_zero-shot_|Vision|0.495|0.363|0.570|0.402|0.540|0.467|**0.590**|0.485|
||T2SP(Ours)|**0.505**|**0.368**|**0.660**|**0.587**|0.480|0.386|0.550|**0.529**|
||Raw|0.563|0.544|0.640|0.506|**0.555**|**0.553**|0.630|0.432|
|_1-shot_|Vision|0.415|0.405|0.630|0.432|0.515|0.445|0.630|0.563|
||T2SP(Ours)|**0.620**|**0.611**|**0.670**|**0.526**|0.550|0.549|**0.710**|**0.703**|
||Raw|0.630|0.617|0.620|0.382|0.590|0.571|0.580|0.554|
|_3-shot_|Vision|0.495|0.412|0.670|0.474|0.650|0.648|0.590|0.580|
||T2SP(Ours)|**0.835**|**0.835**|**0.690**|**0.634**|**0.825**|**0.825**|**0.650**|**0.645**|
||Raw|0.690|0.689|0.630|0.469|0.770|0.770|0.470|0.467|
|_5-shot_|Vision|0.520|0.417|0.590|0.516|0.690|0.689|0.550|0.549|
||T2SP(Ours)|**0.850**|**0.849**|**0.710**|**0.596**|**0.850**|**0.849**|**0.740**|**0.721**|
||Raw|0.650|0.633|0.650|0.442|0.845|0.843|0.610|0.588|
|_20-shot_|Vision|0.560|0.546|0.650|0.442|0.715|0.715|0.700|0.665|
||T2SP(Ours)|**0.895**|**0.894**|**0.730**|**0.668**|**0.900**|**0.899**|**0.760**|**0.736**|



Table 8: **Caption-based classification across LLM backbones.** Comparison of Gemini-3.1-flash-lite and Claude-haiku-4.5 under the same datasets, few-shot protocol, and sampled test sets. For each representation, captions are first generated from the time series, and classification is performed using only the generated captions. Acc and F1 denote accuracy and macro-F1, respectively. 

### **C.1 Time-series Editing Examples** 

We provide examples of the edited time series from the ETTh1 dataset in Figure 7. 

15 

## **D Time-series Captioning** 

<mark>- amplitude: strength of oscillation</mark> 

- <mark>period: length of one cycle</mark> 

We provide the full captioning results in Table 8. 

### **D.1 Time-series Captioning Examples** 

   - <mark>phase: horizontal shift of the wave</mark> 

- <mark>r2: goodness-of-fit of the sinusoidal component (higher means the periodic pattern explains the signal well)</mark> 

- <mark>- optional start_time/end_time indicate the knot (time) interval where the oscillation is active</mark> 

- <mark>- GaussianEvent(center, width, amplitude) - represents localized transient events</mark> 

   - <mark>center: where the event occurs</mark> 

   - <mark>width: how spread the event is over time</mark> 


![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0016-09.png)


   - <mark>amplitude: magnitude of the event</mark> 

- <mark>SpikeEvent(index, amplitude) - represents instantaneous sharp anomalies</mark> 

   - <mark>index: time of occurrence</mark> 

   - <mark>amplitude: magnitude of the spike</mark> 

- <mark>Residual(std) - represents unexplained noise</mark> 

- <mark>std: noise intensity</mark> 

- <mark>The final time series is obtained by combining all components additively. Each component has a clear semantic meaning, and the structured program representation provides a structured, interpretable representation of the signal.</mark> 


![](representing_time_series_as_structured_programs_images/representing_time_series_as_structured_programs.pdf-0016-16.png)


Figure 8: **Captioning results.** 

- <mark># Editing Instruction: Flatten the trend to be constant over time. # Original Program: Series( trend=BSplineTrend( degree=1, smoothness=5, knot_mode='fixed', knots=[0, 0, 31, 31], coeff=[-0.1972, 1.4], n_knots=2, uniform_knots=[0, 31], knot_ts_values=[-0.3627, 1.076]</mark> 

- <mark>), periodic=[ Sinusoid(amplitude=1.7361, period=4, phase=0.6494,</mark> 

- <mark>frequency=0.25, r2=0.9812)</mark> 

- <mark>], events=[ # none</mark> 

- <mark>], noise=Residual(std=0.1698, mean=0)</mark> 

- <mark>) # Rules:</mark> 

- <mark>Provide your reasoning in the <Reason> ... </Reason> section, but do NOT include any code there.</mark> 

- <mark>- Wrap the program in <program> ... </program> tags.</mark> 

<mark>Your answer should be formatted as follows: <Reason></mark> 

## **E Prompts** 

- <mark>Provide your reasoning here, explaining how you modified the original program to satisfy the editing instruction.</mark> 

- <mark>Be specific about which parts of the program you changed and why. </Reason></mark> 

- <mark><program></mark> 

Listing 1: Prompt for Editing Task (TSEdit-Trend) 

<mark>Output your edited program code here. Return ONLY the modified program code. </program></mark> 

<mark>=========================================</mark> 

<mark>Sample ID : trend_L32_0000 Category : trend Edit type : edit_flatten Instruction: Flatten the trend to be constant over time.</mark> 

## **F Use of LLM Assistance** 

<mark>=========================================</mark> 

<mark>You are a time-series program editing expert.</mark> 

<mark>Your task is to modify the symbolic program that represents a time series so that it satisfies the editing instruction below.</mark> 

<mark># Description of the structured program representation The structured program representation is composed of the below interpretable components:</mark> 

We used Claude for sentence-level editing and for coding assistance. All scientific content, experimental design, and conclusions are the authors’ own. 

- <mark>BSplineTrend(degree, knots, coeff)</mark> 

   - <mark>represents the smooth baseline trend over time</mark> 

   - <mark>degree: the degree of the B-spline (e.g., 1 for linear, 3 for cubic. Should always be >= 1)</mark> 

   - <mark>knots: define where the trend is allowed to change its shape (change points in time)</mark> 

   - <mark>uniform_knots: (used only when knot_mode=fixed) human-readable representative knot positions; knots is the full spline knot vector used internally, often with repeated boundary knots</mark> 

   - <mark>coeff:</mark> 

   - <mark>when n_knots == 2: represent the endpoint values of a global</mark> 

   - <mark>linear trend, i.e., coeff = [at_{zero} + b, at_{one} + b] for y = at + b</mark> 

   - <mark>when n_knots > 2: define the spline as a linear combination</mark> 

   - <mark>y(t) = sum_i c_i B_i(t), where coeff = c_i are the basis weights controlling local shape</mark> 

   - <mark>knot_ts_value: the time-series value at each knot. This is the actual value (containing the noise).</mark> 

- <mark>Sinusoid(amplitude, period, phase[, start_time, end_time])</mark> 

   - <mark>represents periodic oscillations</mark> 

16 

