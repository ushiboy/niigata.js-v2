const assert = require('power-assert');
const chrome = require('selenium-webdriver/chrome');
const {Builder} = require('selenium-webdriver');
import {FishesList} from './PageObject.js';

describe('FishList', function() {

  this.timeout(20000);

  let driver;

  beforeEach(() => {
    driver = new Builder()
      .forBrowser('chrome')
      .setChromeOptions(new chrome.Options().headless())
      .build();
  });

  afterEach(() => {
    return driver.quit();
  });

  it('一覧が動的に読み込まれること', async () => {
    const p = new FishesList(driver);
    await p.open();
    await p.waitForRowToFinishLoading();

    const rows = await p.getRows();

    assert(rows.length === 3);

    assert(await rows[0].getName() === 'まぐろ')
    assert(await rows[1].getName() === 'はまち')
    assert(await rows[2].getName() === 'かつお')
  });

  it('未選択状態で"けってい"するとアラートがでること', async () => {
    const p =  new FishesList(driver);
    await p.open();
    await p.waitForRowToFinishLoading();

    const alert = await p.clickSelect();
    assert(await alert.getText() === 'せんたくしてください');
  });

  it('一覧のアイテムを1件選択して"けってい"すると選択結果が表示されること', async () => {
    const p =  new FishesList(driver);
    await p.open();
    await p.waitForRowToFinishLoading();

    const rows = await p.getRows();
    await rows[0].clickCheckBox(0);

    const alert = await p.clickSelect();
    assert(await alert.getText() === 'まぐろ');
  });

  it('一覧のアイテムを複数件選択して"けってい"すると選択結果が表示されること', async () => {
    const p =  new FishesList(driver);
    await p.open();
    await p.waitForRowToFinishLoading();

    const rows = await p.getRows();
    await rows[1].clickCheckBox();
    await rows[0].clickCheckBox();

    const alert = await p.clickSelect();
    assert(await alert.getText() === 'まぐろ,はまち');
  });

  it('全体チェックをするとすべてのアイテムが選択されること', async () => {
    const p =  new FishesList(driver);
    await p.open();
    await p.waitForRowToFinishLoading();

    const rows = await p.getRows();
    await rows[0].clickCheckBox();
    const alert1 = await p.clickSelect();
    assert(await alert1.getText() === 'まぐろ');

    await alert1.accept();
    await p.clickAllCheck();

    const alert2 = await p.clickSelect();
    assert(await alert2.getText() === 'まぐろ,はまち,かつお');
  });

  it('全部チェックを外すとすべてのアイテムが選択解除になること', async () => {
    const p =  new FishesList(driver);
    await p.open();
    await p.waitForRowToFinishLoading();

    const rows = await p.getRows();
    await rows[0].clickCheckBox();
    await rows[1].clickCheckBox();
    await rows[2].clickCheckBox();

    const alert1 = await p.clickSelect();
    assert(await alert1.getText() === 'まぐろ,はまち,かつお');

    await alert1.accept();
    await p.clickAllCheck();

    const alert2 = await p.clickSelect();
    assert(await alert2.getText() === 'せんたくしてください');
  });
});
