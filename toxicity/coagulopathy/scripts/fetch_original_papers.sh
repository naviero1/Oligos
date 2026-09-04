#!/usr/bin/env bash
# Download the original source documents that can be fetched without a subscription.
#
#   bash toxicity/coagulopathy/scripts/fetch_original_papers.sh [OUTDIR]
#
# Default OUTDIR is toxicity/coagulopathy/originals/ (git-ignored).
# Sources with no direct URL -- FDA review packages, EMA assessment reports, and every
# publisher-restricted paper -- are NOT fetched here: open the landing_url in
# sources/DOWNLOAD_MANIFEST.csv, which for restricted papers is where your
# institutional access applies.
set -uo pipefail
OUT="${1:-$(dirname "$0")/../originals}"
mkdir -p "$OUT"
ok=0; fail=0
get() {  # get <name> <url>
  if [ -s "$OUT/$1" ]; then echo "  have  $1"; return; fi
  if curl -fsSL --max-time 180 -A "OligoTox-Coagulopathy/1.0" -o "$OUT/$1" "$2"; then
    echo "  got   $1"; ok=$((ok+1))
  else
    echo "  FAIL  $1  <- $2"; rm -f "$OUT/$1"; fail=$((fail+1))
  fi
}
echo "Fetching 53 original documents into $OUT"
get "COG-S001_Nimjee-SM-de-Lange-F-Pitoc-GA-Sullenger-BA-Rats-subject-to-e.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12208382/fullTextXML"
get "COG-S003_Ay-C-Pabinger-I-Kovacevic-KD-et-al-The-VWF-binding-aptamer-r.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9631691/fullTextXML"
get "COG-S008_Ali-AS-et-al-New-High-Affinity-Thrombin-Aptamers-for-Advanci.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10526462/fullTextXML"
get "COG-S009_Yu-H-Pitoc-G-Zhang-M-et-al-An-Aptamer-Based-EXACT-Anticoagul.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12822440/fullTextXML"
get "COG-S010_Yu-H-et-al-Aptameric-hirudins-as-selective-and-reversible-EX.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11087511/fullTextXML"
get "COG-S011_Reed-CR-Bonadonna-D-Otto-JC-McDaniel-CG-Chabata-CV-Kuchibhat.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8728519/fullTextXML"
get "COG-S012_Kolyadko-VN-Layzer-JM-Perry-K-Sullenger-BA-Krishnaswamy-S-An.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11260126/fullTextXML"
get "COG-S013_Kandimalla-E-R-Manning-A-Agrawal-S-et-al-Mixed-backbone-anti.pdf" "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/5886165"
get "COG-S014_Crooke-S-T-et-al-Antidotes-to-antisense-compounds-United-Sta.pdf" "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8389488"
get "COG-S015_Archemix-Corp-Aptamer-therapeutics-useful-in-the-treatment-o.pdf" "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7538211"
get "COG-S017_Jongejan-YK-Dirven-RJ-Schrader-Echeverri-E-de-Jong-AJL-Pronk.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11909755/fullTextXML"
get "COG-S018_Maliglowka-M-Dec-A-Buldak-L-Okopien-B-The-Effects-of-Inclisi.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12470796/fullTextXML"
get "COG-S019_Zhu-X-Li-H-Hu-C-Wu-M-Zhou-S-Wang-Y-Li-W-Safety-analysis-of-l.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11270951/fullTextXML"
get "COG-S020_Stolte-B-Nonnemacher-M-Kizina-K-Bolz-S-Totzeck-A-Thimm-A-Wag.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8563549/fullTextXML"
get "COG-S021_Calcaterra-IL-Santoro-R-Vitelli-N-Cirillo-F-D-Errico-G-Guerr.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11428464/fullTextXML"
get "COG-S022_Demirjian-S-Ailawadi-G-Polinsky-M-Bitran-D-Silberman-S-Shern.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5733816/fullTextXML"
get "COG-S023_Abourahma-H-Kempaiah-P-Farooqui-A-Krupa-E-et-al-A-Comparativ.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13009829/fullTextXML"
get "COG-S024_DEFITELIO-defibrotide-sodium-injection-for-intravenous-use-U.pdf" "https://dailymed.nlm.nih.gov/dailymed/getFile.cfm?setid=2c3db989-d7ad-41ed-9ebf-698dcf6c24ec&type=pdf"
get "COG-S025_Seth-Chhabra-E-Liu-M-Evaluation-of-the-interference-of-fitus.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12451317/fullTextXML"
get "COG-S026_QFITLIA-fitusiran-injection-for-subcutaneous-use-US-Prescrib.pdf" "https://dailymed.nlm.nih.gov/dailymed/getFile.cfm?setid=6dd2f8ac-6f90-4cbf-b197-97d74964135c&type=pdf"
get "COG-S027_Young-G-Kavakli-K-Klamroth-R-et-al-Safety-and-efficacy-of-a.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12824673/fullTextXML"
get "COG-S028_Pipe-SW-Lissitchkov-T-et-al-Long-term-safety-and-efficacy-of.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11914172/fullTextXML"
get "COG-S029_Kenet-G-Nolan-B-Zulfikar-B-et-al-Fitusiran-prophylaxis-in-pe.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11181353/fullTextXML"
get "COG-S030_Young-G-Sorensen-B-Dargaud-Y-et-al-Targeting-of-antithrombin.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8251589/fullTextXML"
get "COG-S031_McCluskey-G-Maynadie-H-Borgel-D-et-al-Fitusiran-treatment-mo.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13146349/fullTextXML"
get "COG-S032_Modulation-of-factor-7-expression-United-States-Patent-US-9.pdf" "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9029337"
get "COG-S033_Modulation-of-prekallikrein-PKK-expression-United-States-Pat.pdf" "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9670492"
get "COG-S034_Serpinc1-iRNA-compositions-and-methods-of-use-thereof-United.pdf" "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9376680"
get "COG-S035_Modulation-of-Factor-11-expression-United-States-Patent-US-1.pdf" "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10772906"
get "COG-S036_Compositions-and-methods-for-inhibiting-gene-expression-of-f.pdf" "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10858658"
get "COG-S037_Methods-for-modulating-factor-12-expression-United-States-Pa.pdf" "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9150864"
get "COG-S038_Walsh-M-Bethune-C-Smyth-A-Tyrwhitt-J-Jung-SW-Yu-RZ-Wang-Y-Ge.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8820988/fullTextXML"
get "COG-S041_Lang-T-Hodel-K-Kubitza-E-et-al-Pharmacokinetics-pharmacodyna.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10985948/fullTextXML"
get "COG-S042_Ferrone-JD-Bhattacharjee-G-Revenko-AS-Zanardi-TA-Warren-MS-D.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6461157/fullTextXML"
get "COG-S043_Liang-J-Nilsson-S-Wikstrom-J-Cao-H-Zheng-S-Xu-Q-Yan-X-Uecker.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12230477/fullTextXML"
get "COG-S045_TEGSEDI-inotersen-injection-for-subcutaneous-use-US-Prescrib.pdf" "https://dailymed.nlm.nih.gov/dailymed/getFile.cfm?setid=8513207e-b55f-417b-9473-af785146a543&type=pdf"
get "COG-S046_RYTELO-imetelstat-for-injection-for-intravenous-use-US-Presc.pdf" "https://dailymed.nlm.nih.gov/dailymed/getFile.cfm?setid=b0fab7ca-e578-43c5-9df6-bdaff4182257&type=pdf"
get "COG-S047_TRYNGOLZA-olezarsen-injection-for-subcutaneous-use-US-Prescr.pdf" "https://dailymed.nlm.nih.gov/dailymed/getFile.cfm?setid=0f51aa8e-8475-8cf9-e063-6394a90a6848&type=pdf"
get "COG-S048_DAWNZERA-donidalorsen-injection-for-subcutaneous-use-US-Pres.pdf" "https://dailymed.nlm.nih.gov/dailymed/getFile.cfm?setid=3ff501e0-f75f-07da-e063-6294a90a0cb7&type=pdf"
get "COG-S049_SPINRAZA-nusinersen-injection-for-intrathecal-use-US-Prescri.pdf" "https://dailymed.nlm.nih.gov/dailymed/getFile.cfm?setid=dd70cd5f-b0fc-4ba4-a5ea-89a34778bd94&type=pdf"
get "COG-S050_NEGATIVE-CONTROL-WAINUA-eplontersen-injection-for-subcutaneo.pdf" "https://dailymed.nlm.nih.gov/dailymed/getFile.cfm?setid=d7dcb847-71dd-4fff-82d0-d43a465fc096&type=pdf"
get "COG-S051_NEGATIVE-CONTROL-QALSODY-tofersen-injection-for-intrathecal.pdf" "https://dailymed.nlm.nih.gov/dailymed/getFile.cfm?setid=81356b45-1cb7-4eef-88ea-e44cc18b47c5&type=pdf"
get "COG-S052_NEGATIVE-CONTROL-ONPATTRO-patisiran-injection-lipid-complex.pdf" "https://dailymed.nlm.nih.gov/dailymed/getFile.cfm?setid=e87ec36f-b4b4-49d4-aea4-d4ffb09b0970&type=pdf"
get "COG-S059_Ohara-M-Nagata-T-Hara-RI-Yoshida-Tanaka-K-Toide-N-Takagi-K-S.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11382116/fullTextXML"
get "COG-S060_Relizani-K-Echevarria-L-Zarrouki-F-Gastaldi-C-Dambrune-C-Aup.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8754652/fullTextXML"
get "COG-S061_Aupy-P-Echevarria-L-Relizani-K-Zarrouki-F-Haeberli-A-Komisar.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7063478/fullTextXML"
get "COG-S065_Schmidt-M-Hagner-N-Marco-A-Koenig-Merediz-SA-Schroff-M-Witti.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4440985/fullTextXML"
get "COG-S066_Peters-S-Wirkert-E-Kuespert-S-Heydn-R-Johannesen-S-Friedrich.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8780845/fullTextXML"
get "COG-S071_Author-byline-not-present-in-the-retrieved-file-and-therefo.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11109470/fullTextXML"
get "COG-S072_Braendli-Baiocco-A-Festag-M-Dumong-Erichsen-K-Persson-R-Miha.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5414856/fullTextXML"
get "COG-S073_Zavyalova-E-Samoylenkova-N-Revishchin-A-Turashev-A-Gordeychu.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5735248/fullTextXML"
get "COG-S074_Nagano-M-Kubota-K-Sakata-A-Nakamura-R-Yoshitomi-T-Wakui-K-Yo.xml" "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10445101/fullTextXML"
get "COG-S075_Monia-BP-Freier-SM-Wancewicz-EV-et-al-assignee-Isis-Pharmace.pdf" "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9061044"
echo
echo "downloaded $ok, failed $fail"
echo "Everything else: see sources/DOWNLOAD_MANIFEST.csv (landing_url)."
