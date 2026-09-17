# Pubblicazione archivio pubblico redatto pilot-03

- Archivio: `studio2-fase03-pilot-v1.tar`
- SHA-256: `8bc9486601d3d0093d9c8782f906417639cfef4de429e021c45bbe182645d80b`
- File del manifest conservati: 77; redatti: 18; invariati: 59
- Redazioni: `REDAZIONI_pilot-v1-public.json`
- Verifica chiavi API: nessuna occorrenza di `api_key`, `bearer` o `password` nei file del pilot.
- Verifica offline: archivio estratto e confrontato con manifest pubblico; SHA del ledger e conteggi/stability gate da ricalcolare sul contenuto pubblico.

Comando autore:

```sh
gh release create studio2-fase03-pilot-v1 studio2-fase03-pilot-v1.tar studio2-fase03-pilot-v1.tar.sha256 -R sorrentinoluca/fot-tep-data
```
