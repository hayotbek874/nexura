# NEXURA Frontend (React + Vite)

## Ishga tushirish

```bash
npm install
copy .env.example .env
npm run dev
```

Frontend manzil: `http://localhost:5173`

## Build

```bash
npm run build
npm run preview
```

## Asosiy fayllar

- `src/App.jsx` — Boot screen, terminal layout, command handling, canvas animatsiyalar
- `src/styles.css` — UI/UX stillar
- `src/main.jsx` — React kirish nuqtasi
- `src/api/client.js` — umumiy HTTP client
- `src/api/securityApi.js` — security endpointlar

## API sozlamasi

- `.env` ichida `VITE_API_BASE_URL` backend URL bo'ladi.
- Default qiymat: `http://localhost:8000/api`

Frontend hozir quyidagi endpointlarni chaqiradi:

- `GET /health`
- `GET /dashboard`
- `GET /modules/:moduleName`
- `POST /scan` (`{ mode: "quick" | "full" }`)
- `POST /block` (`{ ip }`)
- `GET /alerts?live=true|false`

## Yangi terminal imkoniyatlari

- `Auto-completion`: inputga yozishda dinamik suggestion chiqadi (`Tab` bilan tanlanadi, `↑/↓` bilan yuriladi)
- `Context-aware help`: modul ichida `help` yozilsa faqat shu modul buyruqlari chiqadi
- `Session multiplexing`: bir nechta sessiya (`newtab`) va `split on/off` bilan parallel oynalar

### Foydali buyruqlar

- `modules`
- `use recon`
- `use exploit/web`
- `use exploit/network`
- `help`
- `newtab`
- `sessions`
- `split on`
