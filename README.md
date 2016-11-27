# aws-billing-details-analysis

Analyze the AWS detailed billing report

## Usage
``` shell
~ python analyze_aws_details.py ~/Downloads/####-aws-billing-detailed-line-items-with-resources-and-tags-2016-11.csv
```

## Generated charts

Note that these hide the axis labels to preserve privacy. Also note that I plan on cleaning the code up a bit more to improve the grouping of the "UsageType" values to deal with the long tail.

### By layer
![By layer](https://raw.githubusercontent.com/dangoldin/aws-billing-details-analysis/master/static/img/by_layer.png)

### By product name
![By product name](https://raw.githubusercontent.com/dangoldin/aws-billing-details-analysis/master/static/img/by_product_name.png)

### By usage type
![By usage type](https://raw.githubusercontent.com/dangoldin/aws-billing-details-analysis/master/static/img/by_usage_type.png)

### By usage type - top 25
![By usage type - top 25](https://raw.githubusercontent.com/dangoldin/aws-billing-details-analysis/master/static/img/by_usage_type_top_25.png)

### By user name
![By user name](https://raw.githubusercontent.com/dangoldin/aws-billing-details-analysis/master/static/img/by_user_name.png)

### By user name - top 25
![By user name - top 25](https://raw.githubusercontent.com/dangoldin/aws-billing-details-analysis/master/static/img/by_user_name_top_25.png)

### By layer and usage type - top 50
![By layer and usage type top 50](https://raw.githubusercontent.com/dangoldin/aws-billing-details-analysis/master/static/img/by_layer_usage_type_top_50.png)

### By layer and usage type heatmap
![By layer and usage type heatmap](https://raw.githubusercontent.com/dangoldin/aws-billing-details-analysis/master/static/img/by_layer_usage_type_top_heatmap.png)
