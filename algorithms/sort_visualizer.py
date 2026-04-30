"""
sort_visualizer.py - Sorting Algorithm Visualizer

Renders heapsort.mp4 and mergesort.mp4 (1920x1080, 30 fps, 5 s, with audio)
by wrapping the existing sort implementations without modifying them.

Algorithm files used:
    algorithms/heap_sort.py  - HeapSortGames.heap_sort()
    algorithms/merge_sort.py - MergeSort() / _merge()

Data:  N=50 unique integers 1-50, shuffled with seed 42 (generated here).
Run:   python algorithms/sort_visualizer.py

Revision History:
    (ST) 04/29/2026 Create initial file
"""


import os, sys, random, shutil, subprocess, tempfile, wave

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Add parent directory to path so we can import algorithm modules
ALGO_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(ALGO_DIR))

import algorithms.heap_sort  as hs_mod
import algorithms.merge_sort as ms_mod

# Store absolute paths to the imported files for reporting
HS_FILE = os.path.abspath(hs_mod.__file__)
MS_FILE = os.path.abspath(ms_mod.__file__)

# Video and audio settings
N           = 50           # number of elements to sort
FPS         = 30
DURATION    = 5
FRAMES      = FPS * DURATION   # total frames = 150
SAMPLE_RATE = 44100
W, H        = 1920, 1080
CMAP        = plt.cm.plasma    # colormap mapping bar height to color

# Generate shuffled data with a fixed seed so results are reproducible
random.seed(42)
DATA    = random.sample(range(1, N + 1), N)   # 50 unique integers, shuffled
MAX_VAL = N                                    # maximum possible value in the array


class _Score:
    """
    Wrapper object with a .score attribute so HeapSortGames.get_value() works
    when mode is not 'time'.
    """
    __slots__ = ('value', 'score')

    def __init__(self, v):
        # Store the integer value as both value and score
        self.value = self.score = v


class _RecList(list):
    """
    list subclass passed to heap_sort().

    Captures the full array state and the written index after every __setitem__
    so we can replay the sort as an animation. The algorithm itself is never
    modified.
    """

    def __init__(self, items):
        super().__init__(items)

        # Store snapshots as (state: list[int], touched: list[int])
        self.snaps = []

    def __setitem__(self, idx, val):
        """
        Function intercepts every write and records the resulting array state.

        Inputs:
            idx (int): index being written to
            val:       value being written
        """
        # Perform the actual write first
        super().__setitem__(idx, val)

        # Record a snapshot of the array after the write
        if isinstance(idx, int):
            self.snaps.append(([x.value for x in self], [idx]))


def record_heap(values):
    """
    Function runs heap sort on the given values and returns all recorded snapshots.

    Inputs:
        values (list): list of integers to sort

    Outputs:
        snaps (list): list of (state, touched_indices) tuples captured during the sort
    """
    # Wrap each integer in a _Score so heap_sort can read .score
    items = [_Score(v) for v in values]

    # Use _RecList so every swap is captured
    rec = _RecList(items)
    hs_mod.HeapSortGames().heap_sort(rec, mode='score')

    # Return the list of snapshots recorded during the sort
    return rec.snaps


class _SI:
    """
    Sortable item that carries a value and its original index through recursive
    splits so we can reconstruct the global array view after every merge.
    """
    __slots__ = ('value', 'orig')

    def __init__(self, v, idx):
        # Store the value and the position it started at in the original array
        self.value, self.orig = v, idx

    def __le__(self, o): return self.value <= o.value
    def __lt__(self, o): return self.value <  o.value
    def __ge__(self, o): return self.value >= o.value
    def __gt__(self, o): return self.value >  o.value

    def __eq__(self, o):
        return self.value == (o.value if isinstance(o, _SI) else o)


# Module-level state used by the monkey-patched merge function
_ms_snaps: list = []
_ms_state: list = []   # global display array indexed by original position


def _patched_merge(left, right, key, reverse):
    """
    Function is a drop-in replacement for merge_sort._merge that records
    snapshots during execution without changing the sort logic.

    Inputs:
        left    (list): sorted left half
        right   (list): sorted right half
        key:           optional key function for comparisons
        reverse (bool): if True, sort descending

    Outputs:
        result (list): merged and sorted list
    """
    result, i, j = [], 0, 0

    # Merge left and right halves, recording a snapshot before each comparison
    while i < len(left) and j < len(right):
        li, rj = left[i], right[j]

        # Apply key function if one was provided
        lv = key(li) if key else li
        rv = key(rj) if key else rj

        # Capture current global state and highlight the two elements being compared
        _ms_snaps.append((list(_ms_state), [li.orig, rj.orig]))

        # Pick the smaller (or larger in reverse mode) element
        if (lv >= rv) if reverse else (lv <= rv):
            result.append(li)
            i += 1
        else:
            result.append(rj)
            j += 1

    # Append any remaining elements from either half
    result.extend(left[i:])
    result.extend(right[j:])

    # Update the global display array to reflect the merged span.
    # Map the i-th smallest value to the i-th smallest original position
    # because MergeSort always produces sorted output over a contiguous span.
    sorted_pos = sorted(x.orig for x in result)
    for pos, item in zip(sorted_pos, result):
        _ms_state[pos] = item.value

    # Record one final snapshot showing the completed merged span
    _ms_snaps.append((list(_ms_state), sorted_pos))

    return result


def record_merge(values):
    """
    Function runs merge sort on the given values and returns all recorded snapshots.

    Inputs:
        values (list): list of integers to sort

    Outputs:
        snaps (list): list of (state, touched_indices) tuples captured during the sort
    """
    global _ms_snaps, _ms_state

    # Reset snapshot list and initialize display state from the input
    _ms_snaps, _ms_state = [], list(values)

    # Temporarily replace the module's _merge with our recording version
    orig_merge    = ms_mod._merge
    ms_mod._merge = _patched_merge
    try:
        ms_mod.MergeSort([_SI(v, i) for i, v in enumerate(values)])
    finally:
        # Restore the original merge function even if an exception occurs
        ms_mod._merge = orig_merge

    return list(_ms_snaps)


def render_frame(ax, state, touched_set, title, max_val):
    """
    Function draws a single bar-chart frame onto the given axes.

    Inputs:
        ax          (Axes):  matplotlib axes to draw on
        state       (list):  current array values
        touched_set (set):   indices of bars to highlight white
        title       (str):   chart title shown at the top
        max_val     (int):   maximum value, used to scale the y-axis and colors
    """
    # Clear the axes before drawing
    ax.cla()
    ax.set_facecolor('black')

    n = len(state)

    # Assign white to touched bars, colormap color to all others
    col = [
        'white' if i in touched_set
        else CMAP(state[i] / max_val) if max_val else CMAP(0.0)
        for i in range(n)
    ]

    # Draw bars
    ax.bar(range(n), state, color=col, width=0.9, linewidth=0)

    # Set axis limits and labels
    ax.set_xlim(-0.5, n - 0.5)
    ax.set_ylim(0, max_val * 1.08)
    ax.set_title(title, color='white', fontsize=22, fontweight='bold', pad=14)

    # Hide the frame border
    for sp in ax.spines.values():
        sp.set_visible(False)

    ax.tick_params(colors='white')
    ax.set_xlabel('Index', color='#888888', fontsize=11)
    ax.set_ylabel('Value', color='#888888', fontsize=11)


def make_wav(frames, max_val, path):
    """
    Function generates a WAV audio file with one sine burst per frame.
    The frequency of each burst is proportional to the touched bar's value.

    Inputs:
        frames  (list): list of (state, touched_indices) tuples
        max_val (int):  maximum value used to scale frequency (200-1000 Hz)
        path    (str):  output file path for the WAV file
    """
    # Calculate samples per frame and build a linear ramp envelope to avoid clicks
    spf  = SAMPLE_RATE // FPS
    ramp = max(1, spf // 10)
    env  = np.ones(spf, dtype=float)
    env[:ramp]  = np.linspace(0, 1, ramp)
    env[-ramp:] = np.linspace(1, 0, ramp)

    chunks = []
    for state, touched in frames:
        # Use the touched bar's value to pick the frequency for this frame
        v    = state[min(touched[0], len(state) - 1)] if touched else max_val // 2
        freq = 200.0 + (v / max_val) * 800.0 if max_val else 440.0

        # Generate one sine burst for this frame and apply the envelope
        t = np.linspace(0, 1.0 / FPS, spf, endpoint=False)
        chunks.append(np.sin(2 * np.pi * freq * t) * env * 0.45)

    # Convert to 16-bit PCM and write to a WAV file
    pcm = (np.concatenate(chunks) * 32767).clip(-32768, 32767).astype(np.int16)
    with wave.open(path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(pcm.tobytes())


def pick_frames(snaps, n_frames):
    """
    Function selects exactly n_frames snapshots from the full snapshot list.
    Evenly samples if there are too many steps; holds the final frame if too few.

    Inputs:
        snaps    (list): all recorded snapshots
        n_frames (int):  desired number of frames

    Outputs:
        result (list): list of exactly n_frames snapshots
    """
    # Return empty list if there are no snapshots
    if not snaps:
        return []

    total = len(snaps)

    # Sample evenly if we have more snapshots than frames needed
    if total >= n_frames:
        return [snaps[int(k * (total - 1) / (n_frames - 1))] for k in range(n_frames)]

    # Pad with the final snapshot if we have fewer snapshots than frames needed
    result = list(snaps)
    while len(result) < n_frames:
        result.append(snaps[-1])

    return result


def build_video(snaps, title, outfile, max_val):
    """
    Function renders a full MP4 video with audio from a list of sort snapshots.

    Inputs:
        snaps   (list): list of (state, touched_indices) tuples
        title   (str):  label shown on the chart
        outfile (str):  output file path for the MP4
        max_val (int):  maximum array value used for scaling
    """
    # Select the frames we will actually render
    frames = pick_frames(snaps, FRAMES)

    # Use a temporary directory to hold intermediate files
    tmp = tempfile.mkdtemp(prefix='sortvis_')
    try:
        # Define paths for intermediate files
        wav  = os.path.join(tmp, 'audio.wav')
        raw  = os.path.join(tmp, 'video_raw.mp4')
        fdir = os.path.join(tmp, 'frames')
        os.makedirs(fdir)

        # Generate the audio track
        make_wav(frames, max_val, wav)

        # Create the figure with a black background
        fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
        fig.patch.set_facecolor('black')
        ax  = fig.add_axes([0.06, 0.10, 0.88, 0.80])

        # Render each frame as a PNG image
        print(f'  Rendering {len(frames)} frames...')
        for fi, (state, touched) in enumerate(frames):
            render_frame(ax, state, set(touched), title, max_val)
            fig.savefig(os.path.join(fdir, f'{fi:05d}.png'),
                        dpi=100, facecolor='black')
        plt.close(fig)

        # Combine the PNG frames into a raw video file using ffmpeg
        subprocess.run([
            FFMPEG, '-y', '-r', str(FPS),
            '-i', os.path.join(fdir, '%05d.png'),
            '-vf', f'scale={W}:{H}',
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'fast',
            raw,
        ], check=True, capture_output=True)

        # Mux the video and audio into the final output file
        subprocess.run([
            FFMPEG, '-y',
            '-i', raw, '-i', wav,
            '-c:v', 'copy', '-c:a', 'aac', '-shortest',
            outfile,
        ], check=True, capture_output=True)

    finally:
        # Always clean up temporary files even if rendering fails
        shutil.rmtree(tmp, ignore_errors=True)


def _ffmpeg_exe():
    """
    Function returns the path to the ffmpeg binary.
    Checks the system PATH first, then falls back to the imageio_ffmpeg bundle.

    Outputs:
        exe (str): path to the ffmpeg executable
    """
    # Check if ffmpeg is available on the system PATH
    exe = shutil.which('ffmpeg')
    if exe:
        return exe

    # Fall back to the bundled ffmpeg from imageio_ffmpeg if installed
    try:
        import imageio_ffmpeg  # type: ignore[import-untyped]
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit('ERROR: ffmpeg not found. Install ffmpeg or run: pip install imageio-ffmpeg')


# Resolve the ffmpeg path once at module load time
FFMPEG = _ffmpeg_exe()


def main():
    """
    Function renders heapsort.mp4 and mergesort.mp4 into the algorithms directory.
    """
    # Print the source files and data configuration being used
    print('Algorithm files used:')
    print(f'  HeapSort  : {HS_FILE}')
    print(f'  MergeSort : {MS_FILE}')
    print(f'Data        : N={N}, values=random.sample(range(1,{N+1}),{N}), seed=42')
    print(f'Target      : {FRAMES} frames @ {FPS} fps ({DURATION} s)\n')

    # Record and render the heap sort visualization
    print('[HeapSort]')
    hs_snaps = record_heap(list(DATA))
    print(f'  Raw snapshots : {len(hs_snaps)}')
    hs_out = os.path.join(ALGO_DIR, 'heapsort.mp4')
    build_video(hs_snaps, 'Heap Sort', hs_out, MAX_VAL)
    print(f'  Output        : {hs_out}')

    # Record and render the merge sort visualization
    print('\n[MergeSort]')
    ms_snaps = record_merge(list(DATA))
    print(f'  Raw snapshots : {len(ms_snaps)}')
    ms_out = os.path.join(ALGO_DIR, 'mergesort.mp4')
    build_video(ms_snaps, 'Merge Sort', ms_out, MAX_VAL)
    print(f'  Output        : {ms_out}')

    print('\nDone.')


if __name__ == '__main__':
    main()
