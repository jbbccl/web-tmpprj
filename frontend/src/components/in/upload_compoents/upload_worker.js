import axios from 'axios';

import _ from 'lodash'

function uploadChunk(chunk){
    return axios.post('/api/home/upload_f',
        chunk,{
        headers: {
        'Content-Type': 'multipart/form-data',
      }}).then(res=>{
        postMessage(1)
      });
}


onmessage = async (e)=>{
    const{
        rst,
        start,
        end
    } = e.data;
    const file_name=rst[1];
    const chunks=rst[0];
    const proms=[];
    for(let i = start; i<end;i++){
        //console.log('name is: '+file_name);
        chunks[i]['file_name']=file_name;
        //console.log(chunks[i]);
        proms.push(uploadChunk(chunks[i]));
    }
    let up_result = await Promise.all(proms);
    postMessage(32);//关闭码
    //全部处理完返回./uploadfiles
}