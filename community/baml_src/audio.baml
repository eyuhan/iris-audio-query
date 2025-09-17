function QueryAudio(
    query: string,
    audio_files: audio[]
) -> string {
    client "openai/gpt-audio"

    prompt #"
You are an AI assistant helping answer user queries based on audio files.

The user asked:
`{{query}}`

Below are audio files retrieved from an audio embedding search. Each file is semantically relevant to the query.

{% for file in audio_files %}
  {{ file }}
{% endfor %}

Using these audio files, compose a clear and accurate answer to the user's question.

Do not make up information — only answer based on the provided audio files.

{{ ctx.output_format }}
"#
}
