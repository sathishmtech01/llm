    huggingface-cli login
    huggingface-cli download google/flan-t5-small --local-dir ./flan-t5-small

    For the data provided, the best approach is to fine-tune a pre-trained encoder-decoder model like T5 (Text-to-Text Transfer Transformer) or BART specifically for abstractive text summarization. 
    These models are designed for sequence-to-sequence tasks and are ideal for generating concise, fluent, and meaningful summaries
