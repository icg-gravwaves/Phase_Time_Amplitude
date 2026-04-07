WORKFLOW_NAME=o3
CHUNKNUMBER=35 # Change as appropriate
CONFIG_TAG=v2.3.14.6 # Change as appropriate
DESCRIPTION='Original' # (NOTE: no spaces, INITIAL recommended for first run)
GITLAB_URL="https://git.ligo.org/pycbc/offline-analysis/-/raw/${CONFIG_TAG}"
CONFIG_URL="$GITLAB_URL/production/o4/broad/config"
BANK_URL="$GITLAB_URL/production/o4/broad/compress_bank"

# Make sure no proxy is present before creating scitokens and kinit
ecp-get-cert --destroy
htdestroytoken
kinit
unset XDG_RUNTIME_DIR
htgettoken -a vault.ligo.org -i igwn
export GWDATAFIND_SERVER="datafind.ligo.org:443"

PYCBC_COMMAND="pycbc_make_offline_search_workflow \\
  --workflow-name ${WORKFLOW_NAME} \\
  --output-dir output \\
  --cache-file \\
  ${BANK_URL}/reuse_banks.cache \\
  --config-overrides \\
      results_page:output-path:\"/home/${USER}/public_html/pycbc/o3/runs/broad/a${CHUNKNUMBER}_${DESCRIPTION}\" \\
  --submit-now \\
  --config-files \\
  ${CONFIG_URL}/analysis.ini \\
  data_O4_HLV_C00_AR.ini \\
  ${CONFIG_URL}/executables_common.ini \\
  ${CONFIG_URL}/executables_osg.ini \\
  ${CONFIG_URL}/executables_for_scitokens.ini \\
  gps_times_chunk${CHUNKNUMBER}.ini \\
  injections_chunk${CHUNKNUMBER}.ini \\
  ${CONFIG_URL}/injections_common.ini \\
  ${CONFIG_URL}/inspiral.ini \\
  ${CONFIG_URL}/plotting.ini"

# Add special configs for statistic tuning options
if [[ "${CHUNKNUMBER}" == "24" || "${CHUNKNUMBER}" == "25" ]]; then
  PYCBC_COMMAND+=" \\
  ${CONFIG_URL}/analysis_LV.ini"
elif [[ "${CHUNKNUMBER}" == "30" ]]; then
  PYCBC_COMMAND+=" \\
  ${CONFIG_URL}/analysis_HV.ini"
else
  PYCBC_COMMAND+=" \\
  ${CONFIG_URL}/analysis_HLV.ini"
fi

eval "$PYCBC_COMMAND"
