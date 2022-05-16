hname=$(hostname)
echo $hname
full_string="gcloud compute instances list --format \"get(zone)\" --filter=\"$hname\""
echo $full_string
eval url=\$\($full_string\)
project=$(echo $url | cut -d/ -f7)
echo $project

#crear regla de vpc
rule_string="gcloud compute --project=$project firewall-rules create mariadb --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:3306 --source-ranges=0.0.0.0/0 --target-tags=mariadb"
echo $rule_string
eval $rule_string

#obtener zona de instancia actual
full_string="gcloud compute instances list --format \"get(zone)\" --filter=\"$hname\""
echo $full_string
eval url=\$\($full_string\)
zone=$(echo $url | cut -d/ -f9)
echo $zone

#agregar tag de  vpc a instancia actual
tag_string="gcloud compute instances add-tags \"$hname\" --zone \"$zone\" --tags mariadb"
echo $tag_string
eval $tag_string
