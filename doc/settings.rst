========
環境設定
========

Requirements
============

- Python 3.5
- Graphviz 2.38
- Sphinx 1.4

インストール
============

--------------
Graphvizの導入
--------------

本拡張はGraphvizを利用しています。
そのため、別途、Graphvizを入手しインストールを実施してください。

------------------
拡張のインストール
------------------

続いて、pipでモジュールのインストールを行います。

.. code-block:: bat

   pip install sphinx_erdiagram

ビルドの設定
============

| conf.pyにて、拡張の設定を記述します。
| `sphinx.ext.graphviz拡張 <http://docs.sphinx-users.jp/ext/graphviz.html>`_ で利用できるプロパティを使用することができます。

.. code-block:: python

   extensions = ['myasuda.sphinx.erdiagram']
   graphviz_output_format = "svg"       #出力形式を指定します。(Defaultではpng)


**graphviz_dotプロパティ**

dotを呼び出すときに使用するコマンド名を指定できます。デフォルトでは 'dot' となります。

.. note::

   | このプロパティは異なる環境で共通で利用できないため、通常、conf.pyの中で設定しません。
   | 以下のように、sphinx-buildコマンドの `-D <http://docs.sphinx-users.jp/invocation.html#cmdoption-sphinx-build-D>`_ オプションとして利用します。

   .. code-block:: bat

      sphinx-build -b html -D graphviz_dot=C:\graphviz\bin\dot.exe . _build/html
