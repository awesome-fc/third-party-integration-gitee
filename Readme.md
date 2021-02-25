# FC Integrated With Gitee Callback Demo

This demo introduce a demo to intrgrate [Gitee](https://gitee.com/) with FunctionCompute using Gitee http callback to invoke function, and then function can read the Gitee event, such as code submmit, new commont. Gitee will send the corresponding event to function HTTP URL, then function read the event to upload code to OSS.

![](https://congxiao.oss-cn-beijing.aliyuncs.com/Untitled%20Diagram%20%282%29.png)

## Step1: Prepare the environment
1. Install [Funcraft](https://help.aliyun.com/document_detail/140283.html?spm=a2c4g.11186623.6.820.6a034e21y2jlx1) on the local machine. For more information, see installation instructions.
  - Run `fun --version` to check whether the installation is successful.
  - You need to configure funcraft with your own aliyun access key id and access key secret. Follow the steps in Configure Funcraft .Run fun config to configure Funcraft. Then configure Account ID, Access Key ID, Access Key Secret, and Default region name as prompted.

```
$ fun config
Aliyun Account ID 1234xxx
Aliyun Access Key ID xxxx
Aliyun Access Key Secret xxxx
Default region name cn-xxxx
The timeout in seconds for each SDK client invoking 300
The maximum number of retries for each SDK client 5
Allow to anonynously report usage statistics to improve the tool over time? (Y/n)

```
2. Enter [Gitee](https://gitee.com/) webhook, and put your `id_rsa.pub` to Gitee SSH.

3. Open OSS service: 
  - Create a bucket
  - Upload the `id_rsa` and `my_ssh_executable.sh` file to bucket
4. Open FC service

## Step2: Deploy function
1. Run following command on the demo root path：

 ```
fun deploy -y # deploy function
```

## Step3: Test

Set the function URL to the Gitee webhook URL, and then trigger the event following, you will see the code is upload to your OSS bucket.

![](https://congxiao.oss-cn-beijing.aliyuncs.com/%E6%88%AA%E5%B1%8F2021-02-24%20%E4%B8%8B%E5%8D%8812.59.06.png)

