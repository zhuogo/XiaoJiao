import { useState, type CSSProperties } from 'react'
import benchPalettes from './data/benchgo-palettes.json'
import BenchPaletteGallery from './BenchPaletteGallery'
import './go-family.css'

type Mode = 'mark' | 'app' | 'mono'
const defaultBenchPalette = benchPalettes.find(p => p.default)!
const products = [
  {id:'draftgo',name:'DraftGo',role:'开发底座',type:'容器模式 / Web 系统',color:'#244DE0',bg:'#E9EEFA',idea:'让创造，有自己的运行空间。',detail:'蓝色轨道穿行于小角前后，橙色模块是正在搭建的系统。连接、容纳，承托整个产品家族。',colors:['#244DE0','#EE9853','#F1F5FF'],version:'已定方向',path:'/logos/go/'},
  {id:'routergo',name:'RouterGo',role:'模型连接',type:'模型服务 / 统一 API',color:'#B94332',bg:'#F6EAE3',idea:'一个入口，连接更多可能。',detail:'延续原来的暖红小角与分流线路。箭头指向调用，端点代表连接，多家模型在同一个入口相遇。',colors:['#B94332','#F08D70','#FFF6EE'],version:'原方案',path:'/logos/go/v2/'},
  {id:'selfgo',name:'SelfGo',role:'思考画布',type:'个人笔记 / 知识整理',color:'#265B4C',bg:'#E6EDE3',idea:'把思绪，一页页收好。',detail:'完整的小角坐在前景，错落的画布从身后露出。松绿与纸白留出安静的空间，容纳笔记、闪念和逐渐成形的想法。',colors:['#265B4C','#80A68C','#F1F3E7'],version:'画布叠层',path:'/logos/go/v2/'},
  {id:'benchgo',name:'BenchGo',role:'全天候助手',type:'本地 AI / 办公与开发',color:defaultBenchPalette.wordmark,bg:defaultBenchPalette.background,idea:'想法就绪，随时开工。',detail:defaultBenchPalette.detail,colors:[defaultBenchPalette.color,defaultBenchPalette.accent,defaultBenchPalette.paper],version:defaultBenchPalette.name,path:'/logos/go/v2/'}
]

export default function GoFamily(){
  const [mode,setMode]=useState<Mode>('mark')
  const [benchPaletteId,setBenchPaletteId]=useState(defaultBenchPalette.id)
  const benchPalette=benchPalettes.find(p=>p.id===benchPaletteId)??defaultBenchPalette
  const visibleProducts=products.map(p=>p.id==='benchgo'?{...p,asset:benchPalette.stem,color:benchPalette.wordmark,bg:benchPalette.background,detail:benchPalette.detail,colors:[benchPalette.color,benchPalette.accent,benchPalette.paper],version:benchPalette.default?benchPalette.name+' · 当前方案':'配色参照'}:{...p,asset:p.id})
  return <><section id="go-family" className="go-family" aria-labelledby="go-title">
    <div className="go-heading">
      <div><p className="go-eyebrow">小角 / GO PRODUCT FAMILY</p><h1 id="go-title">同一个小角，<br/>四种产品性格。</h1><p className="go-sub">开发底座 · 模型连接 · 思考画布 · 全天候助手</p></div>
      <div className="go-actions"><div className="go-switch" role="group" aria-label="家族图标形式">{([['mark','品牌标志'],['app','应用图标'],['mono','单色检查']] as const).map(([id,title])=><button key={id} type="button" aria-pressed={mode===id} className={mode===id?'selected':''} onClick={()=>setMode(id)}>{title}</button>)}</div><a className="go-bundle" href="/logos/go/v2/go-family-v2.zip" download>下载家族图标包 ↗</a></div>
    </div>
    <div className="go-grid">{visibleProducts.map((p,index)=><article key={p.id} id={'brand-'+p.id} style={{'--go-color':p.color,'--go-bg':p.bg} as CSSProperties}>
      <div className={'go-art go-art-'+mode}>
        <div className="go-art-top"><span>0{index+1} / {p.role}</span><span>{p.version}</span></div>
        <a className="go-image-link" href={p.path+(mode==='mono'?p.id:p.asset)+'-'+mode+'.svg'} target="_blank" rel="noreferrer" aria-label={'放大查看 '+p.name+' '+(mode==='app'?'应用图标':mode==='mono'?'单色标志':'品牌标志')}><img src={p.path+(mode==='mono'?p.id:p.asset)+'-'+mode+'.svg'} alt={p.name+' 小角品牌图标'+(p.id==='benchgo'?' · '+benchPalette.name:'')}/></a>
        <div className="go-signature"><strong>{p.name}</strong><span>{p.type}</span></div>
      </div>
      <div className="go-description"><h2>{p.idea}</h2><p>{p.detail}</p>
        {p.id==='benchgo'&&<div className="go-palette-picker"><div className="go-palette-label"><label htmlFor="bench-palette-select">预览配色</label><a href="#benchgo-palettes">查看全部 {benchPalettes.length} 款 ↘</a></div><select id="bench-palette-select" className="go-palette-select" value={benchPaletteId} onChange={e=>setBenchPaletteId(e.target.value)}>{benchPalettes.map(palette=><option key={palette.id} value={palette.id}>{palette.name}{palette.default?'（当前方案）':''} · {palette.color}</option>)}</select></div>}
        <div className="go-specimens"><div className="go-small-icons" aria-label={p.name+' 小尺寸预览'}>{[16,32,48].map(size=><img key={size} src={p.id==='selfgo'||p.id==='benchgo'?p.path+p.asset+'-icon-'+size+'.png':p.path+p.id+'-app.svg'} width={size} height={size} alt={size+' 像素预览'} title={size+' px'}/>)}</div><div className="go-colors" aria-label="品牌色">{p.colors.map(color=><span key={color} title={color} style={{background:color}}/>)}</div></div>
        <div className="go-links"><a href={'https://'+p.id+'.cn'} target="_blank" rel="noreferrer">{p.id}.cn ↗</a><a href={p.path+(mode==='mono'?p.id:p.asset)+'-'+mode+'.svg'} download>SVG ↓</a><a href={p.path+(mode==='mono'?p.id:p.asset)+'-'+mode+'.png'} download>PNG ↓</a></div>
        {p.id==='benchgo'&&<div className="go-revision-links"><a href={p.path+'benchgo-final.zip'} download>原配色图标包 ↓</a><a href={p.path+'benchgo-palette-board.png'} target="_blank" rel="noreferrer">全部配色展板 ↗</a><a href={p.path+'benchgo-comparison.png'} target="_blank" rel="noreferrer">形态调整对比 ↗</a></div>}
      </div>
    </article>)}</div>
    <div className="go-footnote"><p>熟悉的身体、双眼与切角。让产品的个性，生长在小角周围。</p><a href="/logos/go/v2/go-family-board.png" target="_blank" rel="noreferrer">查看完整对比图 ↗</a></div>
  </section><BenchPaletteGallery selectedId={benchPaletteId} onSelect={setBenchPaletteId}/></>
}
