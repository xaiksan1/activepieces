# 🔥 ACTIVEPIECES - Alexandria Integration Plan

## 🎯 Qu'est-ce qu'Activepieces?

**L'Alternative Open Source à Zapier** - Automatisation visuelle no-code avec 280+ intégrations!

### 🌟 Pourquoi c'est PARFAIT pour Alexandria:

1. **280+ Pieces (Intégrations)** 
   - GitHub, Google, Slack, Discord, Telegram, Email, HTTP, Webhooks...
   - **60% contribuées par la communauté!**
   - Toutes disponibles comme **MCP servers** pour Claude/Cursor/Windsurf!

2. **AI-First Architecture**
   - Support natif: Anthropic, OpenAI, Google AI, Azure, Replicate
   - AI SDK intégré pour créer des agents
   - Copilot pour construire des flows

3. **TypeScript avec Hot Reload** 🔥
   - Développement de pieces custom en temps réel
   - Type-safe, npm packages
   - Meilleure DX possible!

4. **Human-in-the-Loop**
   - Approval workflows
   - Chat Interface trigger
   - Form Interface trigger
   - Delay execution

5. **Enterprise Features**
   - Self-hosted & network-gapped
   - Full branding customization
   - Versioned flows
   - Multi-language support

## 🏗️ Architecture Actuelle (dans le repo)

```
activepieces/
├── docker-compose.yml        # Stack complet
├── .env                       # Configuration
├── packages/                  # Monorepo
│   ├── react-ui/             # Frontend (React)
│   ├── server-api/           # Backend API
│   ├── engine/               # Flow execution engine
│   ├── cli/                  # CLI tools
│   └── pieces/               # 280+ integrations
├── tools/                     # Build & deployment tools
└── docs/                      # Documentation complète
```

### Services Docker Actuels:
```yaml
activepieces:    # Port 8080 (Frontend + API)
postgres:        # Database
redis:           # Queue & cache
```

## 🎯 Integration avec Alexandria

### Phase 1: Déploiement Standalone
```yaml
# Ajouter à alexandria-core/docker-compose.yml
activepieces:
  image: ghcr.io/activepieces/activepieces:0.70.2
  container_name: alexandria-activepieces
  restart: unless-stopped
  ports:
    - "9030:80"  # Interface web
  environment:
    - AP_EXECUTION_MODE=UNSANDBOXED
    - AP_POSTGRES_DATABASE=activepieces
    - AP_POSTGRES_PASSWORD=${ACTIVEPIECES_DB_PASSWORD}
    - AP_POSTGRES_USERNAME=activepieces
    - AP_POSTGRES_HOST=activepieces-postgres
    - AP_REDIS_URL=redis://activepieces-redis:6379
    - AP_FRONTEND_URL=http://localhost:9030
    - AP_TELEMETRY_ENABLED=false
    - AP_SIGN_UP_ENABLED=false  # Sécurité
  volumes:
    - activepieces-cache:/usr/src/app/cache
  networks:
    - internal-secure
    - activepieces-net
  depends_on:
    - activepieces-postgres
    - activepieces-redis

activepieces-postgres:
  image: postgres:14.4
  container_name: alexandria-activepieces-db
  restart: unless-stopped
  environment:
    - POSTGRES_DB=activepieces
    - POSTGRES_PASSWORD=${ACTIVEPIECES_DB_PASSWORD}
    - POSTGRES_USER=activepieces
  volumes:
    - activepieces-postgres:/var/lib/postgresql/data
  networks:
    - activepieces-net

activepieces-redis:
  image: redis:7.0.7
  container_name: alexandria-activepieces-redis
  restart: unless-stopped
  volumes:
    - activepieces-redis:/data
  networks:
    - activepieces-net
```

### Phase 2: Custom Pieces pour Alexandria

Créer des pieces custom pour connecter aux services Alexandria:

#### 1. **@alexandria/aegis-piece**
```typescript
// packages/pieces/alexandria-aegis/src/index.ts
export const aegis = createPiece({
  displayName: 'Alexandria Aegis',
  auth: PieceAuth.SecretText({
    displayName: 'Aegis API Key',
    required: true,
  }),
  actions: [
    createAction({
      name: 'sign_data',
      displayName: 'Sign Data with Aegis',
      description: 'Create cryptographic signature',
      props: {
        data: Property.ShortText({
          displayName: 'Data to Sign',
          required: true,
        }),
      },
      async run(context) {
        const response = await fetch('http://aegis:7000/api/sign', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${context.auth}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ data: context.propsValue.data }),
        });
        return response.json();
      },
    }),
    // verify_signature, rotate_keys, etc.
  ],
});
```

#### 2. **@alexandria/sentinelle-piece**
```typescript
export const sentinelle = createPiece({
  displayName: 'Alexandria Sentinelle',
  actions: [
    createAction({
      name: 'check_threat',
      displayName: 'Check for Threats',
      description: 'Analyze data for security threats',
      // ...
    }),
    createAction({
      name: 'train_model',
      displayName: 'Train ML Model',
      description: 'Submit training data to Sentinelle',
      // ...
    }),
  ],
  triggers: [
    createTrigger({
      name: 'threat_detected',
      displayName: 'When Threat Detected',
      type: TriggerStrategy.WEBHOOK,
      // ...
    }),
  ],
});
```

#### 3. **@alexandria/zangetsu-piece**
```typescript
export const zangetsu = createPiece({
  displayName: 'Alexandria Zangetsu',
  actions: [
    createAction({
      name: 'analyze_blockchain',
      displayName: 'Analyze Blockchain Data',
      // ...
    }),
    createAction({
      name: 'mint_nft',
      displayName: 'Mint NFT',
      // ...
    }),
  ],
});
```

### Phase 3: Workflows Alexandria → Activepieces

#### Workflow 1: Threat Detection Pipeline
```
Webhook (attack detected)
  → Sentinelle Analysis
  → Paint Shop (create pixel)
  → Aegis (sign)
  → Chapel XVI (backup)
  → Slack/Discord notification
```

#### Workflow 2: NFT Minting Automation
```
Form Submit (NFT metadata)
  → Zangetsu (mint on blockchain)
  → Aegis (sign transaction)
  → IPFS upload
  → Twitter announcement
  → Email confirmation
```

#### Workflow 3: AI Agent Orchestration
```
Chat Interface
  → OpenAI/Anthropic (process)
  → genkit flow (execute)
  → Store results (MinIO)
  → Send to user (Email/SMS/Slack)
```

### Phase 4: MCP Server Integration

Activepieces expose automatiquement tous les pieces comme MCP servers!

```json
// Claude Desktop config
{
  "mcpServers": {
    "activepieces-alexandria": {
      "command": "npx",
      "args": [
        "@activepieces/pieces-community",
        "mcp",
        "--pieces",
        "alexandria-aegis,alexandria-sentinelle,alexandria-zangetsu"
      ]
    }
  }
}
```

## 🚀 Déploiement Rapide

### Option 1: Docker Compose (Recommandé)
```bash
cd /home/ichigo/alexandria/anima-mundi/backend/defense/alexandria-core

# Créer .env pour activepieces
cat > activepieces/.env << 'EOF'
AP_EXECUTION_MODE=UNSANDBOXED
AP_POSTGRES_DATABASE=activepieces
AP_POSTGRES_PASSWORD=$(openssl rand -base64 32)
AP_POSTGRES_USERNAME=activepieces
AP_POSTGRES_HOST=activepieces-postgres
AP_REDIS_URL=redis://activepieces-redis:6379
AP_FRONTEND_URL=http://localhost:9030
AP_TELEMETRY_ENABLED=false
AP_SIGN_UP_ENABLED=false
AP_ENCRYPTION_KEY=$(openssl rand -base64 32)
AP_JWT_SECRET=$(openssl rand -base64 32)
EOF

# Merger avec docker-compose principal
# (voir configuration Phase 1 ci-dessus)

# Démarrer
docker-compose up -d activepieces activepieces-postgres activepieces-redis
```

### Option 2: Développement Local
```bash
cd activepieces
npm install
npm run dev

# Frontend: http://localhost:4200
# Backend: http://localhost:3000
# Engine: http://localhost:3001
```

## 🎯 Use Cases Alexandria

1. **Security Automation**
   - Auto-respond to threats detected by Sentinelle
   - Rotate keys on schedule (Aegis)
   - Backup critical data (Chapel XVI)

2. **Blockchain Operations**
   - Auto-mint NFTs when conditions met
   - Monitor blockchain events → trigger actions
   - Update metadata across platforms

3. **AI Workflows**
   - Process user inputs through multiple AI providers
   - Chain genkit flows with external APIs
   - Human approval for sensitive operations

4. **DevOps Automation**
   - Deploy on git push
   - Run tests → notify on Slack
   - Auto-scale services based on metrics

5. **User Notifications**
   - Multi-channel: Email, SMS, Slack, Discord, Telegram
   - Template-based messages
   - Scheduled reports

## 📊 Benefits pour Alexandria

| Feature | Before | After (avec Activepieces) |
|---------|--------|---------------------------|
| **Integrations** | Custom code pour chaque | 280+ pieces prêtes |
| **Automation** | Scripts bash/Node.js | Visual no-code builder |
| **AI Providers** | Fragmented API calls | Unified AI SDK |
| **Notifications** | Manual implementation | 10+ channels instant |
| **Human Approval** | Custom implementation | Built-in workflows |
| **Observability** | Logs only | Visual flow execution |
| **Team Collaboration** | Dev only | Non-tech users too |

## 🔐 Security Considerations

1. **Network Isolation**
   - Activepieces dans `internal-secure` network
   - Pieces Alexandria n'exposent pas de secrets
   - API keys stockés encrypted dans DB

2. **Authentication**
   - Disable sign-up (`AP_SIGN_UP_ENABLED=false`)
   - Single admin user
   - JWT tokens pour API access

3. **Execution Mode**
   - `UNSANDBOXED` pour accès aux services internes
   - Rate limiting sur webhooks
   - Input validation stricte

## 📈 Next Steps

1. ✅ **Immediate**: Deploy Activepieces standalone
2. ✅ **Week 1**: Create custom Alexandria pieces
3. ✅ **Week 2**: Build 5 critical workflows
4. ✅ **Week 3**: Enable MCP server integration
5. ✅ **Week 4**: Team training & documentation

## 🎓 Learning Resources

- [Official Docs](https://www.activepieces.com/docs)
- [Create a Piece](https://www.activepieces.com/docs/developers/building-pieces/overview)
- [Discord Community](https://discord.gg/2jUXBKDdP8)
- [280+ Existing Pieces](https://www.activepieces.com/pieces)

---

**STATUS: Ready for BANKAI integration** ⚡

Activepieces = Le cerveau d'automatisation visuelle d'Alexandria 🧠
