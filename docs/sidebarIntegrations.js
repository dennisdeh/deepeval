module.exports = {
  integrations: [
    {
      type: "category",
      label: "Model Providers",
      items: [
        "model-openai",
        "model-azure-openai",
        "model-anthropic",
        "model-gemini",
        "model-vertex-ai",
        "model-ollama",
        "model-vllm",
        "model-lmstudio",
      ],
      collapsed: false,
    },
    {
      type: "category",
      label: "Frameworks",
      items: [
        "framework-llamaindex",
      ],
      collapsed: false,
    },
    {
      type: "category",
      label: "Vector Databases",
      items: [
        "vectordb-cognee",
        "vectordb-elasticsearch",
        "vectordb-chroma",
        "vectordb-weaviate",
        "vectordb-qdrant",
        "vectordb-pgvector",
      ],
      collapsed: false,
    },
  ],
};
