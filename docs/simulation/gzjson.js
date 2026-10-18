// 2026-10-19：大型行情檔改存 .json.gz 省站台體積。GitHub Pages 對 .gz 不加 Content-Encoding，
// 瀏覽器拿到的是原始 gzip 位元組，要自己解壓。
// 開頭是 gzip 魔術位元組（1f 8b）就解壓，否則當純文字 JSON；所以同一個函式也能讀沒壓縮的清單檔，
// 萬一哪天主機或快取層改成自動解壓，也不會壞。
export async function gzJson(response){
  if(typeof response.arrayBuffer!=='function')return response.json();
  const bytes=new Uint8Array(await response.arrayBuffer());
  if(bytes.length>1&&bytes[0]===0x1f&&bytes[1]===0x8b){
    if(typeof DecompressionStream!=='function')throw Error('這個瀏覽器不支援解壓縮行情檔，請更新瀏覽器。');
    const stream=new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'));
    return JSON.parse(await new Response(stream).text());
  }
  return JSON.parse(new TextDecoder().decode(bytes));
}
