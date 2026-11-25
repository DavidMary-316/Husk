# Husk

Remove hidden location, phone and time data from your photos and videos before you post or send them.

**Live site:** https://husk.fragmentsofsilent.workers.dev/

Free, no ads, no tracking. Everything runs in your browser. Your files are never uploaded.

## What it does

- Works with JPEG, PNG, WebP, MP4 and MOV.
- You choose what to remove: **Location, Device, Time, Camera settings, People & notes, Other**. Nothing switched on means nothing is changed.
- Shows exactly what was found and removed, what was changed (for example a replaced date), what was kept, and what was not present.
- Optional: replace the date inside the file with a random one, and use neutral file names.
- Photos are rewritten without moving the picture data. Videos are cleaned in place without re-encoding, so quality is unchanged.
- Every cleaned file is scanned a second time, and the result tells you if anything selected is still there.

## Check it yourself

You do not have to trust the author. Husk is one HTML file.

1. **No network.** `husk.html` has a Content-Security-Policy that blocks every outgoing connection (`connect-src 'none'`). Open the file in a text editor and search for `fetch`, `XMLHttpRequest`, `WebSocket` and `sendBeacon`. There are no calls.
2. **Airplane mode test.** Download `husk.html`, switch on airplane mode, open it, and clean a photo. It still works.
3. **Checksum.** `SHA256SUMS.txt` lists the SHA-256 of `husk.html`. Compare your copy:
   - Windows: `certutil -hashfile husk.html SHA256`
   - Mac / Linux: `shasum -a 256 husk.html`
4. **Rebuild it.** The files in `husk.html` and `site/` are built from `src/husk-source.html` and give identical bytes:
   ```
   python3 build/build_standalone.py
   python3 build/build_site.py
   ```
   (Python 3, no extra packages.)
5. **Check the result.** Clean a photo, then open the copy in any metadata viewer and confirm the data you selected is gone.

## What is here

| Path | What it is |
| --- | --- |
| `husk.html` | The single-file offline copy. Download this and open it. |
| `site/` | The website as published: page, service worker, manifest, icons, security headers. |
| `src/husk-source.html` | The master source the other files are built from. |
| `build/` | The two small scripts that build `husk.html` and `site/`. |
| `SHA256SUMS.txt` | Checksums of the built files. |

## Limits

- Removes data stored **in the file**. It cannot hide what the picture shows: faces, street signs, reflections.
- Cannot remove invisible watermarks or a camera sensor's noise pattern.
- The encoder name written inside a video stream cannot be removed without re-encoding.
- HEIC photos are not supported yet (export as JPEG first). WebM, MKV and AVI videos are not supported.
- File names like `IMG_20261114_064109` can reveal a date. Use the neutral file names option.
- Messaging apps and email usually send the original file, so clean it before sharing.
- This is a one-person project and has **not been independently audited**. There are no automated tests in this repository yet.

## Support

Husk is free. If it helped you and you would like to support more free tools, you can do that on Ko-fi: https://ko-fi.com/fragmentsofsilent. It is entirely optional.

## Bugs and ideas

Open an Issue. Bug reports and ideas are welcome. Code contributions are not being accepted for now.

## Licence

See `LICENSE`. Copyright (c) 2026 DavidMary-316.
