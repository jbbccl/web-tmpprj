import SparkMD5 from 'spark-md5'

function creatChunk(file,index,SIZE){
    //console.log('超级探针==+++-----------1??3----------------')
    return new Promise((resolve)=>{
        const start = index*SIZE;
        const end = start+SIZE;
        const spark = new SparkMD5.ArrayBuffer();
        const fileReader = new FileReader();
        const blob = file.slice(start,end);
        fileReader.onload = (e)=>{
            spark.append(e.target.result);

            resolve({
                blob,
                start,
                end,
                index,
                hash:spark.end(),
            });
        };//blob为空报错
        fileReader.readAsArrayBuffer(blob);//异步 结束后回调 fileReader.onload = (e)=>{
    })
};

onmessage = async (e)=>{
    const{
        file,
        SIZE,
        start_chunk:start,
        end_chunk:end
    } = e.data;
    //console.log(file,start,end);
    const proms=[];

    for(let i = start; i<end;i++){
        proms.push(creatChunk(file,i,SIZE));
        
    }
    let chunks=[];
   // console.log('超级探针==+++-----------1113----------------')
    chunks = await Promise.all(proms);
    //console.log('超级探针==+++-----------1123----------------')
    //console.log(chunks)
    postMessage(chunks)//全部处理完返回
}
