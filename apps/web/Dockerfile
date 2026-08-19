FROM node:22-bookworm-slim

WORKDIR /app

COPY apps/web/package.json apps/web/pnpm-lock.yaml ./
RUN npm install --global pnpm@10.6.3 && pnpm install --frozen-lockfile

COPY apps/web ./

EXPOSE 5201

CMD ["pnpm", "dev", "--", "--host", "0.0.0.0", "--port", "5201"]
