import { useEffect, useRef, useState, type CSSProperties } from 'react'
import { createRoot } from 'react-dom/client'
import studies from './data/form-studies.json'
import palettes from './data/benchgo-palettes.json'
import { assetUrl } from './asset-url'
import './gallery.css'

type Mode = 'mark' | 'app' | 'mono'
type Asset = { id: string; name: string; group: string; svg: string; png: string | null; preview?: string; pdf?: string; bundle?: string; guide?: string; boardBundle?: string; fileCount?: number }
type Exhibit = { name: string; description: string; color: string; root: string; base?: string; bundle?: string }
const root = '/logos/go/v2/'
const products = [
  { id: 'draftgo', name: 'DraftGo', role: '开发底座', line: '让创造，有自己的空间。', description: '蓝色轨道穿过小角，连接正在搭建的系统。', color: '#E7ECF7', ink: '#244DE0', stem: 'draftgo' },
  { id: 'routergo', name: 'RouterGo', role: '模型连接', line: '一个入口，更多可能。', description: '暖红色的分流线路，让模型在同一个入口相遇。', color: '#F2E4DF', ink: '#A53E30', stem: 'routergo' },
  { id: 'selfgo', name: 'SelfGo', role: '思考画布', line: '把思绪，一页页收好。', description: '松绿画布轻轻叠起，留住笔记、闪念和想法。', color: '#E3EBDD', ink: '#265B4C', stem: 'selfgo' },
  { id: 'benchgo', name: 'BenchGo', role: '全天候助手', line: '想法就绪，随时开工。', description: '熟悉的编辑器标签与光标，陪伴每一次办公与开发。', color: '#E8EAE5', ink: '#343B36', stem: 'benchgo-original' },
]
const modes: [Mode, string][] = [['mark', '品牌标志'], ['app', '应用图标'], ['mono', '单色']]
function Modes({ value, onChange }: { value: Mode; onChange: (value: Mode) => void }) {
  return <div className="switch" aria-label="图标形式">{modes.map(([id, label]) => <button key={id} aria-pressed={value === id} onClick={() => onChange(id)}>{label}</button>)}</div>
}
function Downloads({ svg, png }: { svg: string; png?: string | null }) {
  return <div className="downloads"><a href={assetUrl(svg)} download>下载 {svg.endsWith('.png') ? 'PNG' : 'SVG'} ↓</a>{png && <a href={assetUrl(png)} download>PNG ↓</a>}</div>
}
function App() {
  const [product, setProduct] = useState(0), [mode, setMode] = useState<Mode>('mark')
  const [palette, setPalette] = useState('original'), [paused, setPaused] = useState(false)
  const [exhibit, setExhibit] = useState<Exhibit | null>(null), [detailMode, setDetailMode] = useState<Mode>('mark'), [base, setBase] = useState(false)
  const [assets, setAssets] = useState<Asset[]>([]), [group, setGroup] = useState('基准'), [query, setQuery] = useState(''), [assetError, setAssetError] = useState(false), [retry, setRetry] = useState(0)
  const [asset, setAsset] = useState<Asset | null>(null)
  const dialog = useRef<HTMLDialogElement>(null), returnFocus = useRef<HTMLElement | null>(null)
  const active = products[product], bench = palettes.find(p => p.id === palette)!
  const stem = mode === 'mono' ? active.id : active.id === 'benchgo' ? bench.stem : active.stem
  const image = root + stem + '-' + mode
  const modalOpen = !!(exhibit || asset)
  useEffect(() => {
    const controller = new AbortController()
    setAssetError(false)
    fetch(assetUrl('/assets/catalog.json'), { signal: controller.signal }).then(r => { if (!r.ok) throw Error(); return r.json() }).then(setAssets).catch(e => { if (e.name !== 'AbortError') setAssetError(true) })
    return () => controller.abort()
  }, [retry])
  useEffect(() => {
    if (!modalOpen) return
    returnFocus.current = document.activeElement as HTMLElement
    dialog.current?.showModal()
    const old = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    return () => { document.body.style.overflow = old; dialog.current?.close(); returnFocus.current?.focus() }
  }, [modalOpen])
  useEffect(() => {
    const observer = new IntersectionObserver(entries => entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('arrived'); observer.unobserve(e.target) } }), { threshold: .08 })
    document.querySelectorAll('.reveal').forEach(e => observer.observe(e))
    return () => observer.disconnect()
  }, [])
  function choose(index: number) { setProduct(index); document.getElementById('products')?.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' }) }
  function close() { setExhibit(null); setAsset(null) }
  const detailRoot = exhibit ? (base && exhibit.base ? exhibit.base : exhibit.root) + '-' + detailMode : ''
  const filtered = assets.filter(a => a.group === group && a.name.toLowerCase().includes(query.trim().toLowerCase()))
  return <div className={paused ? 'gallery paused' : 'gallery'}>
    <a className="skip" href="#products">跳到产品图标</a>
    <header className="header"><a className="wordmark" href="#">小角<span>XiaoJiao</span></a><nav aria-label="主导航"><a href="#products">产品</a><a href="#cases">案例</a><a href="#library">资产</a></nav><button className="motion-toggle" aria-pressed={paused} onClick={() => setPaused(!paused)}>{paused ? '播放动态' : '暂停动态'}<span aria-hidden="true">{paused ? ' ▷' : ' Ⅱ'}</span></button></header>
    <main>
      <section className="hero" aria-labelledby="hero-title">
        <div className="hero-title"><h1 id="hero-title">小角，大有不同。</h1><div><p>一个小角，四种产品性格。<br/>在这里，看见图标的更多可能。</p><a className="primary" href="#products">探索产品图标 <span>↘</span></a></div></div>
        <div className="hero-art" aria-label="四个产品图标">{products.map((p, i) => <button className={'hero-object object-' + i} key={p.id} onClick={() => choose(i)} aria-label={'查看 ' + p.name} style={{ '--delay': `${i * -.9}s` } as CSSProperties}><img src={assetUrl(root + p.stem + '-mark.png')} alt={p.name + ' 小角图标'} width="840" height="760" fetchPriority={i === 0 ? 'high' : 'auto'}/><span>{p.name}<span>{p.role}</span></span></button>)}</div>
        <div className="hero-bottom"><span>熟悉的双眼，标志性的切角。</span><span>原创角色与产品图标</span></div>
      </section>
      <section className="product-section" id="products" aria-labelledby="products-title">
        <div className="section-head reveal"><h2 id="products-title">同一个小角。</h2><p>个性，生长在小角周围。</p></div>
        <div className="product-stage" style={{ '--field': active.id === 'benchgo' ? bench.background : active.color, '--product-ink': active.ink } as CSSProperties}>
          <div className="product-tabs" aria-label="选择产品">{products.map((p, i) => <button key={p.id} aria-pressed={product === i} onClick={() => setProduct(i)}>{p.name}<span>{p.role}</span></button>)}</div>
          <div className="product-art" key={image}><img src={assetUrl(image + '.png')} alt={active.name + ' ' + modes.find(m => m[0] === mode)?.[1]} width="840" height="760"/><span className="product-signature">{active.name}</span></div>
          <div className="product-info"><div><h3>{active.line}</h3><p>{active.description}</p></div><div className="product-controls"><Modes value={mode} onChange={setMode}/>{active.id === 'benchgo' && <label className="palette-label">配色<select value={palette} onChange={e => setPalette(e.target.value)} disabled={mode === 'mono'}>{palettes.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}</select></label>}<Downloads svg={image + '.svg'} png={image + '.png'}/></div></div>
        </div>
      </section>
      <section className="cases-section" id="cases" aria-labelledby="cases-title"><div className="section-head reveal"><h2 id="cases-title">不止一种相遇。</h2><p>环绕、叠层、连接、陪伴。<br/>十二种形态，仍然是小角。</p></div>
        <div className="case-wall">{studies.map((s, i) => <button className={'case reveal case-' + i % 4} key={s.id} onClick={() => { setDetailMode('mark'); setBase(false); setExhibit({ name: s.name, description: s.description, color: s.background, root: '/logos/studies/' + s.id, base: '/logos/studies/' + s.id + '-base', bundle: '/logos/studies/' + s.id + '.zip' }) }}><span className="case-image" style={{ background: s.background }}><img loading="lazy" src={assetUrl('/logos/studies/' + s.id + '-mark.png')} alt={s.name} width="840" height="760"/><span className="case-open" aria-hidden="true">↗</span></span><span className="case-caption"><strong>{s.name}</strong><span>{s.usage}</span></span></button>)}</div>
      </section>
      <section className="library-section" id="library" aria-labelledby="library-title"><div className="section-head"><h2 id="library-title">小角的全部。</h2><p>从第一块基板，到每一种表情。<br/>每一份灵感，都在这里。</p></div>
        <div className="library-tools"><div className="library-tabs" aria-label="资产分类">{['基准','表情','装饰','配色','历史','展板'].map(g => <button key={g} aria-pressed={group === g} onClick={() => { setGroup(g); setQuery('') }}>{g}</button>)}</div><input type="search" aria-label="搜索资产" placeholder="搜索资产" value={query} onChange={e => setQuery(e.target.value)}/></div>
        {assetError ? <p role="alert">资产索引加载失败。<button onClick={() => setRetry(r => r + 1)}>重新加载</button></p> : !assets.length ? <p role="status">正在加载资产…</p> : <><div className="asset-grid">{filtered.map(a => <button key={a.id} onClick={() => setAsset(a)}><span><img loading="lazy" src={assetUrl(a.preview || a.png || a.svg)} alt={a.name} width="390" height="280"/></span><strong>{a.name}</strong></button>)}</div>{!filtered.length && <p role="status">没有找到这个名称，试试其他关键词。</p>}</>}
        <div className="library-bottom"><span>源文件、历史方案与完整素材，全部保留。</span><a href={assetUrl('/assets/xiaojiao-assets.zip')} download>下载完整资产包 ↓</a></div>
      </section>
    </main>
    <footer><div><p>有小角的地方，<br/>就有一点不同。</p><a href="#">回到顶部 ↑</a></div><span className="footer-name" aria-hidden="true">XiaoJiao.</span><div className="footer-note"><span>小角原创角色</span><a href={assetUrl('/logos/vi/go-family-vi-assets.zip')} download>四产品完整 VI 资产包 ↓</a><a href={assetUrl('/logos/go/v2/go-family-v2.zip')} download>四个产品图标包 ↓</a></div></footer>
    <dialog ref={dialog} onCancel={close} onClose={close} onClick={e => { if (e.target === e.currentTarget) close() }} aria-labelledby="detail-title"><div className="detail"><button className="close" onClick={close} aria-label="关闭详情" autoFocus>×</button><div className="detail-art" style={{ background: exhibit?.color || '#E9ECE8' }}><img src={exhibit ? assetUrl(detailRoot + '.png') : asset ? assetUrl(asset.png || asset.svg) : undefined} alt={exhibit?.name || asset?.name}/></div><div className="detail-copy"><h2 id="detail-title">{exhibit?.name || asset?.name}</h2>{exhibit ? <><p>{exhibit.description}</p><Modes value={detailMode} onChange={setDetailMode}/><div className="switch"><button aria-pressed={!base} onClick={() => setBase(false)}>完整形态</button><button aria-pressed={base} onClick={() => setBase(true)}>小角基准</button></div><Downloads svg={detailRoot + '.svg'} png={detailRoot + '.png'}/><a href={exhibit.bundle ? assetUrl(exhibit.bundle) : undefined} download>下载整套文件 ↓</a></> : asset && <><p>{asset.guide ? `完整交付 · ${asset.fileCount} 个文件，含六页规范手册、独立标识、平台图标、开发变量与可编辑应用模板。当前图片为展板预览。` : `${asset.group}资产`}</p>{asset.bundle && <a href={assetUrl(asset.bundle)} download>{asset.guide ? '下载完整 VI 资产包 ↓' : '下载展板文件包 ↓'}</a>}{asset.guide && <a href={assetUrl(asset.guide)} download>下载品牌规范手册 ↓</a>}<Downloads svg={asset.svg} png={asset.png}/>{asset.pdf && <a href={assetUrl(asset.pdf)} download>下载展板 PDF ↓</a>}{asset.boardBundle && <a href={assetUrl(asset.boardBundle)} download>仅下载展板文件包 ↓</a>}{asset.pdf && <a href={assetUrl(asset.png || asset.svg)} target="_blank" rel="noreferrer">打开高清展板 ↗</a>}</>}</div></div></dialog>
  </div>
}
createRoot(document.getElementById('root')!).render(<App/> )
