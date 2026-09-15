import ImportedWorker from './worker?worker&inline';
import SparkMD5 from 'spark-md5'

const SIZE=5242880;//这里要和update.vue同步
let THREAD=navigator.hardwareConcurrency || 4
const rst=[]


export function cutFile(file){
    let finish_thread_C=0;//在内部定义否则第二次上传线程无法结束
    let file_name;
    const spark = new SparkMD5();
    return new Promise((resolve)=>{
    const chunkCount=Math.ceil(file.size/SIZE);
    if(chunkCount<THREAD){
        THREAD=chunkCount
    }
    const every_thread_chunkCount=Math.ceil(chunkCount/THREAD);
    console.log('共'+chunkCount)
    for(let i=0;i<THREAD;i++){
        const worker=new ImportedWorker();//创建线程 worker.js
        let start = i*every_thread_chunkCount
        let end=(i+1)*every_thread_chunkCount;
        if(end>chunkCount){
            end=chunkCount;
        }
        worker.postMessage({
            file,
            SIZE,
            start_chunk:start,
            end_chunk:end
        });//进入线程
        worker.onmessage = e=>{//0-49 50-99 100-130  线程返回到这里
            for(let i=start;i<end;i++){
                rst[i]=e.data[i-start];
                //spark.append(rst[i]['hash'])
                /*这样生成的hash不唯一 */
                //spark[i]=rst[i]['hash'];
                //spark.append(rst[i]['hasj'])
                //console.log('HASH:  '+rst[i]['hash']);
               // console.log(spark);
            }

            worker.terminate();//此线程结束
            finish_thread_C++;
            if(finish_thread_C==THREAD){
                for(let i=0;i<chunkCount;i++){
                    spark.append(rst[i]['hash']);
                }
                //console.log(spark);
                file_name=spark.end();
                
                console.log('所有分片线程结束'+file_name)
                resolve([rst,file_name])
            }
        }//worker.onmessage
    }
    })
}