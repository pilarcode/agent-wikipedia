# Claude3 Agent with a tool for searching on wikipedia

##  Usage

* Backend : Fast API 

```bash
	cd app_backend && docker build -t backend .
	cd app_backend && docker run -it -p 8000:8000 backend
```

* Frontend: Gradio Chatbot

```bash
	cd app && docker build -t  front .
	cd app && docker run -it -p 8510:8510 front
```

## Cleanup
```bash
	docker images
	docker rmi -f <image_id>
```

# Reference

- https://github.com/langchain-ai/langchain/blob/master/templates/anthropic-iterative-search/anthropic_iterative_search/
- https://python.langchain.com/docs/modules/agents/how_to/custom_agent/
