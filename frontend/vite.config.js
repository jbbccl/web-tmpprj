import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
server:{
   host: '240e:464:512:2c53:9dd1:e887:521b:45b0',
   port: 5509,
   proxy:{
    '/api':{
      target: 'http://127.0.0.1:8001',
      changeOrigin:true,
      //ws: true,
      secure: false,
      rewrite:(path) => path.replace(/^\/api/, ''),
	//真实ip
      bypass(req, res, options) {
        const proxyURL = options.target + options.rewrite(req.url)
        console.log('proxyURL', proxyURL,process.env.HOST)
        req.headers['x-req-proxyURL'] = proxyURL // 设置未生效
        res.setHeader('x-req-proxyURL', proxyURL) // 设置响应头可以看到
      },
    },
   },
   cors:true,
},
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
