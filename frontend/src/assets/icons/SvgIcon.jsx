export default function SvgIcon({ path, height, width, fill }) {
    return (
        <svg
            xmlns="http://www.w3.org/2000/svg"
            width={width || '18'} height={height || '18'}
            viewBox="0 0 24 24"
            fill={fill || 'none'}
            stroke="currentColor"
            strokeWidth="1"
            strokeLinecap="round"
            strokejoin="round"
            className="feather feather-thumbs-up"
        >
            <path d={path}></path>
        </svg>
    )
}