import type { Metadata } from "next";
import {headers} from "next/headers";
import "./globals.css";
const title="Katalon Automation Health";
const description="Executive automation quality, growth, stability and project performance in one management-ready view.";
export async function generateMetadata():Promise<Metadata>{const h=await headers();const host=h.get("host")||"localhost:3000";const protocol=host.includes("localhost")?"http":"https";const image=`${protocol}://${host}/og.png`;return{title,description,openGraph:{title,description,images:[image]},twitter:{card:"summary_large_image",title,description,images:[image]}}}
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>}
