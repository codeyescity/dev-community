import SharePostSection from './components/SharePostSection';
import Posts from './components/Posts';


export default function Timeline() {
    return (
        <section className="timeline">
            <div className="timeline-container">
            <SharePostSection />
            <Posts />
            </div>
        </section>
    )
}