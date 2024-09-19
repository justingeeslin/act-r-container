#!/bin/bash
set -e
set -m

cd ${HOME}
 
# Start the Jupyter Notebook server in the background
jupyter notebook --NotebookApp.default_url="/notebooks/tutorial.ipynb" --ip=0.0.0.0 --port=8888 --NotebookApp.trust_xheaders=True --NotebookApp.allow_origin=* --NotebookApp.token='' --NotebookApp.password='' &

# Capture the PID of the background process
JUPYTER_PID=$!

# Give the server some time to start
sleep 10

# Check if the Jupyter Notebook server is running
if [[ -d /proc/$JUPYTER_PID ]]; then
   echo "Jupyter Notebook server started successfully."
else
   echo "Failed to start Jupyter Notebook server."
fi

# Optionally, you can wait for the server to finish running, or you can keep the script running
wait $JUPYTER_PID