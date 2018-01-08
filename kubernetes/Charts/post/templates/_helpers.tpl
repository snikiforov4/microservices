{{- define "post.fullname" }}
{{ printf "%s-%s" .Release.Name .Chart.Name }}
{{- end }}

{{- define "post.databaseHost" }}
{{ .Values.databaseHost | default (printf "%s-mongodb" .Release.Name) }}
{{- end }}
