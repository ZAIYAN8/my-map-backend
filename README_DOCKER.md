Quick Docker build and run for this project

Build locally:

```bash
docker build -t sc-datav-static .
```

Run locally:

```bash
docker run -p 8080:80 sc-datav-static
# then open http://localhost:8080 in browser
```

Railway:
- If you push this repo to GitHub and link the repo to Railway, Railway will detect the Dockerfile and build the container automatically.
- Alternatively, configure Railway to use Dockerfile build and deploy.
