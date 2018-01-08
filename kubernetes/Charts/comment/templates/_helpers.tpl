{{- define "comment.fullname" }}
{{- printf "%s-%s" .Release.Name .Chart.Name }}
{{- end }}

{{- define "comment.databaseHost" }}
{{- .Values.databaseHost | default (printf "%s-mongodb" .Release.Name) }}
{{- end }}
