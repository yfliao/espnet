# Espnet 的客語辨認範例  

## 模型架構介紹  
* Comformer架構  
    1.分別使用CNN和self-attention機制獲得局部和全部上下文訊息  
    2.Separable convolution: 將卷積拆分成兩個部分，pointwise Conv & depthwise Conv ，可以大幅減少計算量  
![image](https://github.com/MachineLearningNTUT/taiwanese-tts-supech/assets/111730019/deadae9f-17b4-4ff8-9e0b-1dbe0dab39cd)  

* Branchformer架構  
    1.優化Conformer  
    2.有兩個並行分支的encoder  
        一個分支使用 self-attention 來獲得long-range dependencies  
        一個分支則利用MLP來獲得short-range dependencies  
  ![image-2](https://github.com/MachineLearningNTUT/taiwanese-tts-supech/assets/111730019/6ed63023-5e81-451e-88dc-22e25d10139b)  

*  使用 self-supervised pre-trained models as the front-end  
ESPnet支持從大型預訓練模型（例如 wav2vec 2.0 、 HuBERT或wavlm）中抽取self-supervised speech representations  
這些模型是在大量未標記的聲音上進行預訓練的，這種方法在缺乏資料時特別有用  

範例測試結果(CER)  
1.客語漢字(Conformer)  
|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
|decode_asr_asr_model_valid.acc.ave/test|2187|37473|94.7|4.8|0.4|0.1|5.3|17.1|


2.客語拼音(Conformer)   


3.客語漢字(Conformer+wavlm_large)  
|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
|decode_asr_asr_model_valid.acc.best/test|2187|37473|96.8|2.2|1.0|0.1|3.3|17.4|

4.客語拼音(Conformer+wavlm_large)  
|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
|decode_asr_asr_model_valid.acc.ave/test|2187|210486|98.9|0.9|0.2|0.1|1.2|42.1|
|decode_asr_asr_model_valid.acc.best/test|2187|210486|98.7|1.1|0.3|0.2|1.5|47.1|


