

export default function MessageContext({ context }) {
    const menu = (
        <div
        className="absolute bg-blue-400 w-fit h-32"
        style={{
            top: `${context.position.y}px`,
            left: `${context.position.x}px`
        }}
        >
            {context.message.id}
        </div>
    )

    return context.enabled ? menu : ''
}