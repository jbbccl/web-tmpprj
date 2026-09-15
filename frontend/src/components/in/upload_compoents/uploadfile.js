const THREAD=2//Math.ceil((navigator.hardwareConcurrency || 4)/6)
import ImportedWorker from './upload_worker?worker&inline';
//import {finish_count_add} from './update.vue'

const up_rst=[];
export function uploadFile(rst,chunkCount){
    let finish_thread_C=0;
    const every_thread_chunkCount=Math.ceil(chunkCount/THREAD);
    return new Promise((resolve)=>{   
        for(let i=0;i<THREAD;i++){
        const worker=new ImportedWorker();
        let start = i*every_thread_chunkCount
        let end=(i+1)*every_thread_chunkCount;
        if(end>chunkCount){
            end=chunkCount;
        }
        worker.postMessage({
            rst,
            start,
            end
        });//进入线程
        worker.onmessage = e=>{//0-49 50-99 100-130  线程返回到这里
/*             for(let i=start;i<end;i++){
               // console.log('ed'+e.data+'e'+e)
                up_rst[i]=e.data[i-start];
            } */
            //console.log(e.data)
            if(e.data==1){
                window.finish_count_add();
            }
            else if(e.data===32){
                worker.terminate();//此线程结束
                finish_thread_C++;
                if(finish_thread_C==THREAD){
                    console.log('所有上传线程结束');
                    resolve('up_rst');
                }
            }

        }//worker.onmessage
    }})

}