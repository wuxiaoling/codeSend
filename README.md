# 关于项目

本项目用于批量代码分发

This project is used for batch code distribution

# run

    /dist/codeSend /home 


#注意事项
 
- config.json 配置集群服务器地址和登录信息
    
```
{"目标服务器地址":["目标服务器用户","目标服务器密码","目标服务器目录"]}
```

 
- exclude.txt 配置集群服务器不需要同步的文件
    
```
/test/qq
```

- 同步本地目录方法 目标服务器用户填写"/",其他一样