> Ported from the superseded appendices, re-lettered, with the provenance banner,
> section signs and internal codes removed and cross-references renumbered to the
> four-chapter body. Transcription content is unchanged. Provenance: `outline/REWRITE_MAP.md`.

# APPENDIX C – System architecture and the working demonstrator

---

## PART 1: SECTION TEXT

This appendix has two halves. The first gives the formal structural views of the screening-system
architecture described in chapter 4: a component view, a deployment view, a sequence view of one
screening episode, and the persisted data model. Together they discharge the system-architecture
diagram reserved there. The second shows the working demonstrator in operation, so that the modules
Table C.1 marks as built can be seen doing what the table says they do.

What they are should be stated before they are read. Each is a **design specification**, and the
design is realised only in part. A working demonstrator exists and performs inference on submitted
images, and Table C.1 marks which of the modules drawn here it realises. Everything else on these
pages is specified rather than built.

No deployment of this architecture was tested in a clinical setting, and nothing in these diagrams
is evidence that the system performs as drawn. Every element is traceable to a statement in chapter
4; where that chapter does not fix a detail, the detail is omitted here rather than chosen, so the
diagrams contain no design decision that the dissertation has not made in prose.

The diagrams are given as diagram source in Mermaid notation. The source is the definition of the
diagram; rendering to an image is performed during document conversion.

### C.1 Component view

**Diagram C.1 – Module decomposition with provided and required interfaces.**

```mermaid
flowchart TB
 subgraph EXT_IN["External capture"]
 CAM["Fundus camera<br/>(desk / portable / smartphone-based)"]
 end

 subgraph SYS["Automated DR screening system"]
 ORCH["Orchestration /<br/>Error-Handling"]
 ING["Ingestion"]
 PRE["Preprocessing Engine<br/>8-stage pipeline<br/>(configurable)"]
 INF["Inference<br/>5-class grade"]
 REP["Decision-Support /<br/>Reporting<br/>grade + overlay"]
 UI["Clinician Interface<br/>review, override, audit"]
 DM["Data-Management /<br/>PACS-EHR Integration"]
 end

 subgraph EXT_OUT["Hospital systems"]
 PACS["PACS"]
 EHR["EHR"]
 end

 CAM -->|"image + acquisition metadata"| ING
 ING -->|"validated image"| PRE
 PRE -->|"4-channel tensor"| INF
 INF -->|"grade + class posteriors"| REP
 REP -->|"grade + attention overlay"| UI
 UI -->|"clinician disposition"| DM
 REP -->|"result record"| DM
 DM <-->|"FHIR / HL7, asynchronous"| PACS
 DM <-->|"FHIR / HL7, asynchronous"| EHR

 ORCH -.->|"supervises, retries,<br/>routes failures"| ING
 ORCH -.-> PRE
 ORCH -.-> INF
 ORCH -.-> REP
 ING -.->|"rejected input +<br/>reason"| REP
```

The view is to be read against Table C.1 rather than on its own. The table names what each module
does and says whether the demonstrator realises it, so that no reader takes a drawn box for a built
one.

**Table C.1 – Module, function, and whether the demonstrator realises it.**

| Module | Function | In the demonstrator | Described in |
|---|---|---|---|
| Ingestion | Validates a submitted image and rejects input outside the contract | Built | section 4.2 |
| Preprocessing Engine | Applies the eight stages and exposes the state after each | Built | section 4.2 |
| Inference | Loads a checkpoint and grades at the level of the patient | Built | section 4.2 |
| Decision-Support / Reporting | Returns the grade with an attention overlay | Built | sections 4.2 and 4.3 |
| Clinician Interface | Review, recorded verdict, landmark correction | Built | section 4.3 |
| Data-Management | Persists a per-case record | Built as a local case store; the links to hospital imaging and record systems are specification | sections 4.3 and 4.4 |
| Orchestration / Error-Handling | Routes failures and verifies the pipeline at startup | Built | section 4.2 |
| Identity and access control | Per-user identity, roles, access logging | Specification | section 4.4 |

Two features of the decomposition are structural rather than incidental. The Preprocessing Engine is
a first-class module on the inference path, not a data-preparation utility outside the system
boundary, which is the architectural expression of the dissertation's central position. And the
rejected-input path from Ingestion to Reporting is drawn explicitly, because malformed, low-quality
or out-of-contract input must be handled without silent failure, so a rejection is a reported
outcome rather than an absent result.

### C.2 Deployment view

**Diagram C.2 – Store-and-forward deployment topology.**

```mermaid
flowchart LR
 subgraph PERIPH["Peripheral screening site — resource-limited"]
 direction TB
 P_CAM["Fundus camera"]
 P_NODE["Capture node<br/>no GPU<br/>&lt; 16 GB RAM"]
 P_Q["Local outbound queue<br/>(intermittent link)"]
 P_CAM --> P_NODE --> P_Q
 end

 subgraph CENTRE["Reading centre / regional processing node"]
 direction TB
 C_ING["Ingestion"]
 C_PRE["Preprocessing Engine"]
 C_INF["Inference"]
 C_REP["Decision-Support / Reporting"]
 C_UI["Clinician review workstation"]
 C_ING --> C_PRE --> C_INF --> C_REP --> C_UI
 end

 subgraph HOSP["Hospital information systems"]
 direction TB
 H_PACS["PACS"]
 H_EHR["EHR"]
 end

 P_Q ==>|"store-and-forward<br/>encrypted transfer"| C_ING
 C_UI ==>|"disposition"| H_EHR
 C_REP ==>|"study + result"| H_PACS

 classDef bound fill:none,stroke-dasharray:4 3;
 class PERIPH,CENTRE,HOSP bound;
```

This is the view in which the deployment envelope prunes the design. The peripheral site is
specified to require neither inference acceleration nor a continuous link: capture and queueing are
all that occur there, and the transfer boundary is asynchronous by construction. Inference at the
point of capture is not excluded in principle, but it is not the arrangement specified here, and the
store-and-forward form is chosen because it is the one that survives intermittent connectivity.

What the demonstrator realises of this view is the separation and not the topology. Its client is a
static bundle holding no model, and its service runs where an accelerator is available, so the
machine an operator sits at need not be the machine that computes. The peripheral queue and both
links to hospital systems are drawn here and are not built.

### C.3 Sequence view

**Diagram C.3 – One screening episode, capture to persisted disposition.**

```mermaid
sequenceDiagram
 autonumber
 actor OP as Operator
 participant CAM as Camera
 participant ING as Ingestion
 participant PRE as Preprocessing Engine
 participant INF as Inference
 participant REP as Reporting
 actor CLIN as Clinician
 participant DM as Data-Management

 OP->>CAM: acquire fundus image
 CAM->>ING: image + acquisition metadata
 alt input valid
 ING->>PRE: validated image
 PRE->>PRE: stages 0-5, 7 (fixed transform)
 PRE->>INF: 4-channel tensor
 INF->>REP: five-class grade + posteriors
 REP->>REP: generate post-hoc attention overlay
 REP->>CLIN: grade + overlay (decision support)
 CLIN->>CLIN: interpret#59; may override
 CLIN->>DM: diagnosis + disposition + rationale
 DM->>DM: persist record#59; write audit event
 DM-->>REP: acknowledgement
 else input rejected
 ING->>REP: rejection + reason
 REP->>CLIN: rejection notice, no grade issued
 end
```

Two properties of the ordering are the point of the diagram. The clinician's disposition is the
**terminal** step: the system produces a grade and an accompanying overlay, and the diagnosis is
made by the clinician, who may override the system's output and whose rationale is persisted. The
system is decision support within a physician-in-the-loop paradigm and is not a standalone
diagnostic instrument. And the attention overlay is generated *post hoc*, after the grade, as an
interpretability artefact accompanying it. It indicates regions of high gradient-weighted activation
and does not constitute a pixel-level delineation of pathology or a localisation output.

The rejection branch is drawn because a screening system that fails silently on unusable input is a
different and more dangerous system than one that reports the failure. The demonstrator behaves in
the second way, applying the ingestion protocol of chapter 2.

### C.4 Data view

**Diagram C.4 – Persisted entity model.**

```mermaid
erDiagram
 PATIENT ||--o{ STUDY: "undergoes"
 STUDY ||--o{ IMAGE: "contains"
 DEVICE ||--o{ IMAGE: "captured by"
 IMAGE ||--|| PREPROCESSING_RUN: "transformed by"
 PREPROCESSING_RUN ||--|| INFERENCE: "feeds"
 INFERENCE ||--o| OVERLAY: "accompanied by"
 INFERENCE ||--|| DIAGNOSTIC_RESULT: "proposes"
 CLINICIAN ||--o{ DIAGNOSTIC_RESULT: "adjudicates"
 DIAGNOSTIC_RESULT ||--o{ AUDIT_EVENT: "records"
 PATIENT {
 id identifier PK "patient-identifying"
 demographics attributes "patient-identifying"
 }
 STUDY {
 id identifier PK
 acquisition_context attributes
 }
 IMAGE {
 id identifier PK
 laterality attribute
 acquisition_metadata attributes
 }
 DEVICE {
 id identifier PK
 manufacturer_model attributes
 }
 PREPROCESSING_RUN {
 pipeline_configuration attributes
 stage_parameters attributes
 }
 INFERENCE {
 backbone_identity attribute
 grade attribute
 class_posteriors attributes
 }
 OVERLAY {
 artefact reference "interpretability only"
 }
 DIAGNOSTIC_RESULT {
 proposed_grade attribute
 clinician_grade attribute
 override_flag attribute
 rationale text
 }
 CLINICIAN {
 id identifier PK "identifying"
 }
 AUDIT_EVENT {
 actor attribute
 action attribute
 outcome attribute
 }
```

The entities that carry patient or clinician identity are marked, because that is where the security
requirement concentrates. The design places encryption, authentication, role-based access control,
de-identification and audit at the data-management boundary rather than distributing them across the
modules, and this model is the reason: the identifying attributes are persisted in exactly the
entities that boundary owns. The audit record is modelled as a first-class entity, since an override
channel without a durable record of who overrode what is an accountability mechanism only in name.

The security provisions these entities imply are **GDPR/HIPAA-aligned by design**. They are not a
certified compliance status, no conformity assessment was performed, and no statute is asserted to
be satisfied by this model.

### C.5 The demonstrator in operation

The three figures that follow are of the demonstrator rather than of the design. They are here
because Table C.1 marks seven modules as built, and a table asserting it is worth less than the
system doing it. Each is a capture of the client described in section 4.3, driving the inference
service of section 4.2.

**[FIG-C.1: The submission view, with a patient's two eyes accepted for grading and the preprocessing
stages exposed beneath them — defense/figures/1.png]**

Figure C.1 shows the Ingestion and Preprocessing Engine rows of Table C.1 in operation. Two images
are submitted as one patient, right eye and left, and the panel beneath them steps through the stages
of the pipeline for a selected eye, naming the channels each stage yields. The transform is therefore
inspectable rather than implicit, which is the architectural position of this dissertation carried
into the interface: preprocessing is part of the model and is shown as such, not hidden as
preparation of the data.

**[FIG-C.2: The result view, with the patient-level grade, the posterior over the five grades, the
per-eye predictions and the review controls — defense/figures/2.png]**

Figure C.2 shows the Inference and Decision-Support rows. The system returns a five-class grade at
the level of the patient, with the posterior over all five grades, the referable determination and
the per-eye predictions beneath it. The visualisation panel states its own limit — interpretability
evidence, not clinical lesion localisation — and in this capture reports no overlay available, the
attention map being generated from the checkpoint only when the service can produce one. The controls
that follow put a verdict on the prediction to the clinician, which is the physician-in-the-loop
ordering of Diagram C.3 in its realised form.

**[FIG-C.3: The view after a recorded verdict, with the persisted case, the relabelling buffer and the
totals read back from the case store — defense/figures/3.png]**

Figure C.3 shows the Clinician Interface and Data-Management rows. A verdict is persisted against the
case on the server and appended to a relabelling buffer that can be exported for retraining, and the
totals beneath are read from the case store rather than from the browser session. This is the audit
channel of Diagram C.4 in the form it was built: a local case store, with the links to hospital
imaging and record systems still specification.

### Status of these views

Each of the four diagrams elaborates the decomposition of section 4.1, and each is traceable to it
through Table C.1. None of them is evidence about behaviour. The three figures establish that the
modules marked as built exist and what they do in operation, and nothing beyond that: they are not a
measurement, no latency, throughput or reliability figure may be read from them, and the case counts
visible in them are from a development session rather than from use. No field testing was conducted
in any clinical setting, and nothing in this appendix carries a claim about reliability in service,
clinical utility or regulatory status.

---
