
# Inventory & Sales Management (Vercel - Fixed)

## Local Run
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Deploy on Vercel
```bash
npm i -g vercel
vercel --prod
```

## Notes
- SQLite runs in /tmp due to Vercel serverless limitations
- Tables are created lazily on each request
