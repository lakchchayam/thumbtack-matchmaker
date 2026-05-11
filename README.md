# Thumbtack Matchmaker — AI-Powered Service Provider Matching

![TypeScript](https://img.shields.io/badge/Language-TypeScript-3178C6.svg)
![Next.js](https://img.shields.io/badge/Framework-Next.js-black.svg)
![AI](https://img.shields.io/badge/AI-OpenAI%20%7C%20LangChain-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

An intelligent service provider matching system inspired by Thumbtack's marketplace model. Uses LLM-powered semantic matching to connect customers with the most relevant service providers, going beyond keyword search to understand **intent, context, and nuanced requirements**.

## 🎯 Problem Statement

Traditional marketplace search relies on keyword matching and category filters. This fails when customers describe needs in natural language ("someone who can fix my leaky bathroom faucet in the next 48 hours and won't overcharge me") but providers are indexed by rigid category tags.

This project bridges that gap with AI-powered semantic understanding.

## 🏗️ System Architecture

```
Customer Natural Language Query
    │
    ▼
[Intent Extraction Agent]
    ├── Service type classification
    ├── Location & timing extraction
    ├── Budget signal detection
    └── Urgency scoring
    │
    ▼
[Provider Matching Engine]
    ├── Semantic search over provider profiles (vector similarity)
    ├── Availability filtering (structured DB query)
    ├── Rating & review sentiment scoring
    └── Price range compatibility check
    │
    ▼
[Ranking & Explanation]
    ├── Composite match score (0-100)
    ├── LLM-generated match explanation per provider
    └── Personalized recommendation ordering
```

## 🚀 Key Features

- **Conversational Intake**: Customers describe needs in plain English — the LLM extracts structured requirements (service type, budget, location, timing) automatically.
- **Semantic Provider Search**: Provider profiles are embedded and indexed so that "plumber experienced with old homes" matches providers who list "heritage property plumbing" even without exact keyword overlap.
- **LLM-Generated Explanations**: Each match includes a 2-sentence natural language explanation of why this provider is recommended — not just a score.
- **Real-time Availability**: Structured filter layer queries provider schedules before returning matches, eliminating "phantom availability" issues.

## 🛠️ Tech Stack

- **Frontend**: Next.js 14 (App Router), Tailwind CSS, shadcn/ui
- **AI Layer**: LangChain, OpenAI GPT-4o, function calling for structured extraction
- **Vector Search**: Pinecone for provider profile embeddings
- **Backend API**: Next.js API routes + Node.js
- **Database**: PostgreSQL (provider data, availability) + Prisma ORM

## ⚡ Quick Start

```bash
npm install

# Set environment variables
cp .env.example .env.local
# Fill in: OPENAI_API_KEY, PINECONE_API_KEY, DATABASE_URL

# Run database migrations
npx prisma migrate dev

# Seed sample provider data
npm run seed

# Start development server
npm run dev
```

Visit `http://localhost:3000` and describe what service you need.

## 📸 Usage Example

**Customer input:**
> "I need a reliable electrician to install ceiling fans in 3 bedrooms. I'm in North Toronto, available this weekend, budget around $300."

**System extracts:**
```json
{
  "service": "electrician",
  "task": "ceiling fan installation",
  "quantity": 3,
  "location": "North Toronto",
  "availability": "weekend",
  "budget_max": 300
}
```

**Returns:** Top 5 matched electricians with match scores and explanations.
