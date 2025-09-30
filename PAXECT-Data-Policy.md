# PAXECT Data Policy

PAXECT hanteert een duidelijk beleid voor maximale data- en tekstgrootte per run. Dit garandeert stabiele, voorspelbare prestaties en voorkomt misbruik, net als bij toonaangevende systemen als Kafka, MQTT en gRPC.

## 1. Technisch limiet

- **Default limiet:** maximaal **512 MB** per run of opdracht.
- **Aanpasbaar:** Stel een custom limiet in via een environment variable:
  ```bash
  export PAXECT_MAX_INPUT_MB=8192  # Voor max 8 GB
  ```
- **Foutmelding bij overschrijding:**  
  ```
  ❌ Input size exceeds PAXECT policy limit (default 512 MB). Use PAXECT_MAX_INPUT_MB to adjust.
  ```

## 2. Documentatiebeleid

- Dit limiet geldt per opdracht, plugin of brug.
- Voor grotere datasets: gebruik chunking, streaming, of bestandsuitwisseling.
- Sommige plugins (bijv. Polyglot, AES) kunnen een eigen limiet hanteren; zie de betreffende documentatie.

## 3. Positionering als feature

PAXECT kiest bewust voor een limiet, net als andere professionele data-frameworks. Dit is géén beperking, maar een garantie voor betrouwbaarheid, veiligheid en voorspelbare performance.

> _“PAXECT garandeert stabiele prestaties tot 512 MB per run. Voor enterprise workloads is de limiet eenvoudig aanpasbaar.”_

---

**Vragen of verzoeken? Mail ons of open een GitHub issue!**
