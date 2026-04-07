WORKFLOW_NAME=o4
CHUNKNUMBER=18 # Change as appropriate
CONFIG_TAG=v2.3.14.8 # Change as appropriate
DESCRIPTION='4-det' # (NOTE: no spaces, INITIAL recommended for first run)
GITLAB_URL="https://git.ligo.org/pycbc/offline-analysis/-/raw/${CONFIG_TAG}"
CONFIG_URL="$GITLAB_URL/production/o4/broad/config"
BANK_URL="$GITLAB_URL/production/o4/broad/compress_bank"

# Make sure no proxy is present before creating scitokens and kinit
ecp-get-cert --destroy
htdestroytoken
kinit
# PASSWORD_FILE="/home/rahul.dhurkunde/searches/BBH-precession/PRODUCTION/ALIGNED/my_kinit_pass"
# # --- Authentication & Environment Setup ---
# # Read the password securely and run kinit
# echo "$(cat "$PASSWORD_FILE")" | kinit
# if [ $? -ne 0 ]; then
# echo "Error: kinit failed. Exiting script."
# break # Exit the loop
# fi

unset XDG_RUNTIME_DIR
htgettoken -a vault.ligo.org -i igwn
export GWDATAFIND_SERVER="datafind.ldas.cit:80"

PYCBC_COMMAND="pycbc_make_offline_search_workflow \\
  --workflow-name ${WORKFLOW_NAME} \\
  --output-dir output \\
  --cache-file \\
  reuse_banks.cache \\
  --config-overrides \\
      results_page:output-path:\"/home/${USER}/public_html/pycbc/o4/runs/broad/a${CHUNKNUMBER}_${DESCRIPTION}\" \\
  --submit-now \\
  --config-files \\
  analysis.ini \\
  data_O4_HLVK_C00_AR.ini \\
  executables_common.ini \\
  executables_osg.ini \\
  executables_for_scitokens.ini \\
  gps_times_chunk${CHUNKNUMBER}.ini \\
  minimal_injections.ini \\
  inspiral.ini \\
  plotting.ini"

# Add special configs for statistic tuning options
if [[ "${CHUNKNUMBER}" == "24" || "${CHUNKNUMBER}" == "25" ]]; then
  PYCBC_COMMAND+=" \\
  ${CONFIG_URL}/analysis_LV.ini"
elif [[ "${CHUNKNUMBER}" == "30" ]]; then
  PYCBC_COMMAND+=" \\
  ${CONFIG_URL}/analysis_HV.ini"
else
  PYCBC_COMMAND+=" \\
  analysis_HLVK.ini"
fi

eval "$PYCBC_COMMAND"

