How to for SKF labs in Google Cloud
 
Enroll for Google cloud with your gmail account
http://console.cloud.google.com/
 
Check what your service account is (Compute Engine default service account)
https://console.cloud.google.com/iam-admin/iam
*For the first access a new Service Account should be created 
 
Create a project
https://console.cloud.google.com/projectcreate
*For the first time a default project is already created. One can either  create a new projet or the default one can be updated.
 
Enable Compute Engine API for the Service Account
https://console.developers.google.com/apis

Before proceeding, make sure you have created a GCP Project and installed:
https://cloud.google.com/sdk/docs/downloads-interactive

First we create a generic Firewall rule to allow port 5000 for the labs
gcloud compute --project=skf-labs firewall-rules create labs --direction=INGRESS --priority=1 --network=default --action=ALLOW --rules=tcp:5000 --source-ranges=0.0.0.0/0

Now you are able to run the below command to spin up the lab using google cloud and access it
Replace below the following values with your own:
--project=
--service-account=

Remark, for a more beefier machine replace --machine-type value with 
--machine-type=n1-standard-2

gcloud beta compute --project=REPLACE_WITH_YOUR_OWN instances create-with-container cmd --zone=europe-west1-b --machine-type=f1-micro --subnet=default --network-tier=PREMIUM --metadata=google-logging-enabled=true --maintenance-policy=MIGRATE --service-account=REPLACE_WITH_YOUR_OWN-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append --tags=http-server,https-server --image=cos-stable-72-11316-136-0 --image-project=cos-cloud --boot-disk-size=10GB --boot-disk-type=pd-standard --boot-disk-device-name=cmd-1 --container-image=blabla1337/owasp-skf-lab:command-injection --container-restart-policy=always --labels=container-vm=cos-stable-72-11316-136-0

When it’s done you will see a message like this:
Created [https://www.googleapis.com/compute/beta/projects/skf-labs/zones/europe-west1-b/instances/cmd-1].
NAME   ZONE            MACHINE_TYPE  PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP     STATUS
cmd-1  europe-west1-b  f1-micro                   10.132.0.2   35.241.157.147  RUNNING

Remark: It can take up to 5 min before you can access your Lab, you are now able to access the lab by going to:
http://35.241.157.147:5000

