export async function poll(
    fn: () => any,
    delayOrDelayCallback: number | (() => number),
    shouldStopPolling: () => boolean | Promise<boolean> = () => false
  ): Promise<void> {
    do {
      await fn()

      if (await shouldStopPolling()) {
        break
      }

      const delay = typeof delayOrDelayCallback === 'number' ? delayOrDelayCallback : delayOrDelayCallback()
      await new Promise(resolve => setTimeout(resolve, Math.max(0, delay)))
    } while (!await shouldStopPolling())
  }