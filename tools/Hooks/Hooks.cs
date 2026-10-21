// English patch runtime hooks for DIGITAL DEVIL SAGA Avatar Tuner A's TEST Server.
// Assembly-CSharp.dll is patched (see ../Patcher) to call into these methods.
using System;
using System.Collections.Generic;
using System.IO;
using Socotra.UI;
using UnityEngine;

namespace DDSA_EN
{
    public static class Hooks
    {
        static string _dir;
        static readonly Dictionary<string, sbyte[]> _cache = new Dictionary<string, sbyte[]>();

        static string Dir
        {
            get
            {
                if (_dir == null) _dir = Path.Combine(Application.streamingAssetsPath, "english");
                return _dir;
            }
        }

        // ---- resource overrides: StreamingAssets/english/<name> replaces resource:///res/<name>
        public static sbyte[] GetResource(string filename)
        {
            try
            {
                sbyte[] data;
                if (_cache.TryGetValue(filename, out data)) return data;
                string path = Path.Combine(Dir, filename);
                if (File.Exists(path))
                {
                    byte[] raw = File.ReadAllBytes(path);
                    data = new sbyte[raw.Length];
                    Buffer.BlockCopy(raw, 0, data, 0, raw.Length);
                }
                _cache[filename] = data;
                return data;
            }
            catch (Exception e)
            {
                Debug.LogError("[DDSA_EN] override failed for " + filename + ": " + e);
                return null;
            }
        }

        static bool IsSpace(char c) { return c == ' ' || c == '　'; }

        static bool AtBR(string s, int i) { return string.CompareOrdinal(s, i, "<BR>", 0, 4) == 0; }

        // index just past the word containing position i (stops at space, <BR> or end)
        static int WordEnd(string s, int i)
        {
            while (i < s.Length && !IsSpace(s[i]) && !AtBR(s, i)) i++;
            return i;
        }

        // ---- menu / help text wrapping (replacement for GameCanvas.MakeStringTableBR)
        public static string[] MakeStringTableBR(string text, StFont font, int width)
        {
            var lines = new List<string>();
            foreach (string para in text.Split(new[] { "<BR>" }, StringSplitOptions.None))
            {
                if (font == null) { lines.Add(para); continue; }
                string line = string.Empty;
                int i = 0;
                while (i < para.Length)
                {
                    if (IsSpace(para[i]) && line.Length == 0) { i++; continue; }
                    int start = i;
                    int end;
                    if (IsSpace(para[i])) end = i + 1;
                    else { end = start; while (end < para.Length && !IsSpace(para[end])) end++; }
                    string token = para.Substring(start, end - start);
                    if (line.Length > 0 && font.StringWidth(line + token.TrimEnd()) >= width)
                    {
                        lines.Add(line.TrimEnd());
                        line = string.Empty;
                        continue;
                    }
                    if (line.Length == 0 && font.StringWidth(token) >= width)
                    {
                        // single word wider than the box: hard-break it
                        int n = 1;
                        while (n < token.Length && font.StringWidth(token.Substring(0, n + 1)) < width) n++;
                        lines.Add(token.Substring(0, n));
                        i = start + n;
                        continue;
                    }
                    line += token;
                    i = end;
                }
                lines.Add(line.TrimEnd());
            }
            return lines.ToArray();
        }

        // ---- event (dialogue) typewriter, replacement for GameCanvas._printEventString.
        // Same state machine as the original, but a chunk is only accepted if it does not
        // split a word that would overflow the current line.
        public static bool PrintEventString(GameCanvas gc, object[] work, int mode, string str)
        {
            try
            {
                int[] st = (int[])work[0];
                int[] win = (int[])work[2];
                string[] lineText = (string[])work[4];
                short[] lineX = (short[])work[5];
                short[] lineY = (short[])work[6];
                int[] lineCol = (int[])work[7];
                if (st[3] >= str.Length)
                {
                    st[3] = 0;
                    st[13] = 1;
                    return true;
                }
                StFont font = (StFont)gc.GetDataObject(32);
                int limit = win[2] - gc.data_game[49];
                bool lineEmpty = string.IsNullOrEmpty(lineText[st[12]]);
                // swallow spaces at the start of a wrapped line
                while (lineEmpty && st[3] > 0 && st[3] < str.Length && IsSpace(str[st[3]]))
                    st[3]++;
                if (st[3] >= str.Length)
                {
                    st[3] = 0;
                    st[13] = 1;
                    return true;
                }
                int num = st[31];
                int num2 = 0;
                string text = null;
                while (num > 0)
                {
                    if (st[37] == 0 && AtBR(str, st[3]))
                    {
                        if (st[10] != 0)
                        {
                            num = 0;
                            break;
                        }
                        st[3] += 4;
                    }
                    num2 = num;
                    if (st[3] + num2 > str.Length)
                    {
                        num2 = str.Length - st[3];
                        num = num2;
                        if (num <= 0) break;
                    }
                    text = string.Empty;
                    if (num2 > 0) text = str.Substring(st[3], num2);
                    if (st[37] == 0)
                    {
                        int i = 0;
                        while (i < text.Length && !AtBR(str, st[3] + i)) i++;
                        if (i < text.Length)
                        {
                            text = text.Substring(0, i);
                            num2 = i;
                            num = num2;
                        }
                    }
                    int used = st[10] - lineX[st[12]];
                    bool fits = used + font.StringWidth(text) <= limit;
                    if (num2 <= 1 && text.Length > 0 && gc.data_string[11].IndexOf(text[0]) >= 0) break;
                    if (fits)
                    {
                        int e = st[3] + num2;
                        bool midWord = e < str.Length && !IsSpace(str[e]) && !AtBR(str, e) && !IsSpace(str[e - 1]);
                        if (!midWord) break;
                        int we = WordEnd(str, e);
                        if (used + font.StringWidth(str.Substring(st[3], we - st[3])) <= limit) break;
                        // the word does not fit on this line; if it also starts here on an
                        // empty line it can never fit, so allow a hard break
                        int ws = e;
                        while (ws > st[3] && !IsSpace(str[ws - 1])) ws--;
                        if (ws == st[3] && lineEmpty) break;
                    }
                    num--;
                }
                if (num <= 0)
                {
                    if (!gc._eventNewLine(work))
                    {
                        st[29] = 6;
                        st[30] = 1;
                    }
                }
                else
                {
                    int ln = st[12];
                    if (lineText[ln] == null) lineText[ln] = text;
                    else lineText[ln] += text;
                    lineX[ln] = 0;
                    if (st[13] == 0)
                    {
                        lineX[ln] = (short)((win[2] - font.StringWidth(lineText[ln])) / 2);
                        if (lineX[ln] < 0) lineX[ln] = 0;
                    }
                    lineY[ln] = (short)st[11];
                    lineCol[ln] = st[14];
                    st[10] = lineX[ln] + font.StringWidth(lineText[ln]);
                    st[21] = 0;
                    st[3] += num2;
                    if (mode == 0)
                    {
                        st[31] -= num;
                        if (st[31] <= 0)
                        {
                            st[30] = 1;
                            if (st[22] > 0)
                            {
                                st[0] = 16;
                                st[42] = GameCanvas.Adiv(st[22], 100);
                            }
                        }
                    }
                }
            }
            catch (Exception)
            {
                gc.SetError(15330);
            }
            return false;
        }

        // ---- archive wrapper (title screen / pause menu) runs in "ja" mode because its
        // built-in English data is placeholder; swap the ja column for our English text.
        public static void AfterLoadCSV()
        {
            try
            {
                foreach (var kv in Steezy.Localize.Localization.mDictionary)
                {
                    // values exclude the key column: [ja, en]
                    string[] v = kv.Value;
                    if (kv.Key == "KEY" || v.Length < 2) continue;
                    if (!string.IsNullOrEmpty(v[1])) v[0] = v[1];
                }
            }
            catch (Exception e)
            {
                Debug.LogError("[DDSA_EN] AfterLoadCSV: " + e);
            }
        }

        public static TitleDataModel.TitleData FixTitle(TitleDataModel.TitleData d)
        {
            if (d == null || d.tilteName == null || !d.tilteName.Contains("DIGITAL")) return d;
            d.tilteName = "DIGITAL DEVIL SAGA Avatar Tuner\nA's TEST Server Complete Edition";
            d.aboutGame = "Genre: RPG\nEscape the Tower of Karma, where people devour people.\nTransform into a demon: tear, slaughter and devour your foes!";
            d.releaseData = "Feb 26, 2007";
            return d;
        }

        static Sprite[] _howto;

        public static Sprite[] FixHowToPlay(Sprite[] orig)
        {
            try
            {
                if (orig == null) return orig;
                if (_howto != null && _howto.Length == orig.Length) return _howto;
                var res = new Sprite[orig.Length];
                for (int i = 0; i < orig.Length; i++)
                {
                    res[i] = orig[i];
                    if (orig[i] == null) continue;
                    string path = Path.Combine(Path.Combine(Dir, "howto"), string.Concat(orig[i].name, ".png"));
                    if (!File.Exists(path)) continue;
                    var tex = new Texture2D(2, 2, TextureFormat.RGBA32, false);
                    // via reflection: the Span overload of LoadImage can't be resolved against Unity's corlib
                    typeof(ImageConversion).GetMethod("LoadImage", new[] { typeof(Texture2D), typeof(byte[]), typeof(bool) })
                        .Invoke(null, new object[] { tex, File.ReadAllBytes(path), false });
                    tex.name = orig[i].name;
                    Rect r = orig[i].rect;
                    res[i] = Sprite.Create(tex, new Rect(0, 0, tex.width, tex.height),
                        new Vector2(orig[i].pivot.x / r.width, orig[i].pivot.y / r.height), orig[i].pixelsPerUnit);
                    res[i].name = orig[i].name;
                }
                _howto = res;
                return res;
            }
            catch (Exception e)
            {
                Debug.LogError("[DDSA_EN] FixHowToPlay: " + e);
                return orig;
            }
        }
    }
}
