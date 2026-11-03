# Pending regulatory content: tpa-software-india
Not published. Verify each item against the official source, then ask Claude to restore it.

Post: site/blog/tpa-software-india/index.html

Sources these passages relied on:
- [IRDAI-FAQ] IRDAI, FAQs on Health Insurance Regulations: https://irdai.gov.in/faqs-on-health-insurance-regulations
- [IRDAI-TPA] IRDAI, Requirements for Registering as a TPA (IRDAI (Third Party Administrators - Health Services) Regulations, 2016): https://irdai.gov.in/requirements-for-license-as-a-tpa
- [IRDAI-MC] IRDAI, Master Circular on Health Insurance Business, 29 May 2024: https://irdai.gov.in/documents/37343/365525/%e0%a4%b8%e0%a5%8d%e0%a4%b5%e0%a4%be%e0%a4%b8%e0%a5%8d%e0%a4%a5%e0%a5%8d%e0%a4%af+%e0%a4%ac%e0%a5%80%e0%a4%ae%e0%a4%be+%e0%a4%b5%e0%a5%8d%e0%a4%af%e0%a4%b5%e0%a4%b8%e0%a4%be%e0%a4%af+%e0%a4%aa%e0%a4%b0+%e0%a4%ae%e0%a4%be%e0%a4%b8%e0%a5%8d%e0%a4%9f%e0%a4%b0+%e0%a4%aa%e0%a4%b0%e0%a4%bf%e0%a4%aa%e0%a4%a4%e0%a5%8d%e0%a4%b0+_+Master+Circular++on+Health++Insurance+Business++29052024.pdf/5e707a91-b5de-1ec1-cf18-b66273a6839d?t=1716962621002&version=1.0
- [PIB-DPDP] Press Information Bureau, Government notifies DPDP Rules to empower citizens and protect privacy, November 2025: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2190014
- [MEITY-DPDP] Ministry of Electronics and Information Technology, The Digital Personal Data Protection Act, 2023: https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf

---

## 1. Meta description, og:description and JSON-LD BlogPosting description (head)
Original:
> What TPA software in India must handle, from e-cards and cashless pre-auth to NHCX and DPDP rules, plus buy-vs-build trade-offs and vendor questions.

Source: [PIB-DPDP], [MEITY-DPDP]

## 2. JSON-LD BlogPosting keywords (head)
Original keyword entry removed:
> "DPDP Act 2023"

Source: [MEITY-DPDP]

## 3. Hero lead (H1 section)
Original:
> TPA software in India has to run member enrolment, the hospital network, cashless pre-authorization, reimbursement claims and reporting for several insurers at once, with audit trails and health data protected under the DPDP Act. Arnish AI, a software company based in Shirpur, Maharashtra, builds claim and TPA software and wrote this checklist for buyers.

Source: [MEITY-DPDP]

## 4. Section "What does TPA software need to do in India?" (second paragraph)
Original:
> IRDAI defines a TPA as a company registered with the Authority and engaged by an insurer, for a fee, to provide health services. The decision to settle or reject a claim stays with the insurer. That split matters for software design: the TPA platform prepares and recommends, and the insurer decides.

Source: [IRDAI-FAQ]

## 5. Section "How should the cashless pre-authorization desk work?" (first paragraph)
Original:
> The desk receives a request from a network hospital, checks eligibility and policy terms, and sends a decision back fast enough for the insurer to meet IRDAI's timelines. Under the 2024 Master Circular on Health Insurance Business, insurers must decide on a cashless request within one hour and grant final authorization within three hours of the hospital's discharge request.

Source: [IRDAI-MC]

## 6. Section "How should the cashless pre-authorization desk work?" (second paragraph, first sentence)
Original:
> Those limits apply to the insurer, but the TPA's desk is where most of that hour gets used.

Source: [IRDAI-MC]

## 7. Section "How should the cashless pre-authorization desk work?" (What to check list, first item)
Original:
> A queue sorted by time remaining against the turnaround limit, with alerts before it runs out.

(Reworded to refer to each insurer's turnaround targets instead of the regulatory limit.)
Source: [IRDAI-MC]

## 8. Section "What should call centre and grievance handling include?" (second paragraph)
Original:
> The record should show what the member was told and when, because insurers and the regulator may ask for it.

Source: none cited directly (implied regulator access).

## 9. Section "How should it handle fraud checks, duplicates and audit trails?" (third paragraph)
Original:
> The IRDAI TPA regulations require TPAs to keep proper records of all transactions done for an insurer and to make them available to the insurer and the Authority for inspection. In software terms, that means an audit log that cannot be edited, covering data changes, rule overrides, decisions and who viewed a record.

Source: [IRDAI-TPA]

## 10. Section "How does the DPDP Act 2023 affect TPA software?" (whole section, H2 id="data-protection")
Original H2:
> How does the DPDP Act 2023 affect TPA software?

Original paragraphs:
> A TPA processes health and financial data about policyholders, so the Digital Personal Data Protection Act, 2023 applies to it. The DPDP Rules, 2025 were notified in November 2025 and give organisations an 18-month phased compliance period.

> For software, the practical requirements are clear even where legal interpretation is still settling. The system should record the purpose for which data was collected, restrict access by role and by insurer, encrypt data at rest and in transit, log access, detect and report breaches, and delete or anonymise data when it is no longer needed. Check whether the vendor hosts data in India and who at the vendor can access production data.

Original TOC entry:
> DPDP Act 2023 (link #data-protection)

Source: [PIB-DPDP], [MEITY-DPDP]

## 11. Section "Should a TPA buy software or build its own?" (comparison table row)
Original row:
> Regulatory changes | Vendor updates for all clients | Your team or partner must keep up

Source: none cited directly.

## 12. Section "What questions should you ask any TPA software vendor?" (questions 3 and 7)
Original:
> 3. How does the system track pre-authorization turnaround against IRDAI's limits?

> 7. How do you support DPDP Act duties such as consent records, breach reporting and data deletion?

Source: [IRDAI-MC], [MEITY-DPDP]

## 13. FAQ (visible and FAQPage JSON-LD): "Does a TPA decide whether a health claim is paid?"
Original answer:
> No. Under IRDAI rules the insurer settles or rejects the claim, and a denial must be communicated by the insurer with reasons. The TPA processes the claim, checks documents and policy terms and prepares a recommendation. Good TPA software records which person or rule produced each recommendation so the insurer can review it.

Source: [IRDAI-FAQ]

## 14. FAQ (visible and FAQPage JSON-LD): "Does TPA software need to connect to NHCX?"
Original answer:
> NHCX is the National Health Authority's claims exchange. Whether your platform must connect now depends on current IRDAI direction and on what your insurer clients ask for, so check both. New software should be able to send and receive NHCX's FHIR messages even if you start with a few hospitals.

(Question kept; answer rewritten without the IRDAI reference.)
Source: none cited directly (IRDAI direction on NHCX).

## 15. FAQ (visible and FAQPage JSON-LD): "Does the DPDP Act apply to TPAs?"
Original answer:
> Yes. A TPA processes digital personal data of policyholders, including health information, so the Digital Personal Data Protection Act, 2023 applies to it. The DPDP Rules, 2025 were notified in November 2025 with a phased compliance period of 18 months. TPA software should support consent records, access controls, breach detection and deletion when data is no longer needed.

Source: [PIB-DPDP], [MEITY-DPDP]

## 16. Sources list (removed entries)
> IRDAI, FAQs on Health Insurance Regulations (TPA definition; insurer settles or rejects claims)
> IRDAI, Requirements for Registering as a TPA (IRDAI (Third Party Administrators - Health Services) Regulations, 2016)
> IRDAI, Master Circular on Health Insurance Business, 29 May 2024 (cashless decision within one hour; discharge authorization within three hours)
> Press Information Bureau, Government notifies DPDP Rules to empower citizens and protect privacy, November 2025
> Ministry of Electronics and Information Technology, The Digital Personal Data Protection Act, 2023

URLs as listed at the top of this file.
